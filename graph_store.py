"""
graph_store.py — MongoDB-backed graph store.
Database : graphmind
Collections: datasets · nodes · edges
"""

import uuid
import re
from datetime import datetime, timezone
from typing import Any

from database import collections
from seed_data import SEED_DATASETS


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _strip_mongo(doc: dict) -> dict:
    """Remove MongoDB's internal _id field before returning to the client."""
    doc.pop("_id", None)
    return doc


# ═══════════════════════════════════════════════════════════════════════════════
class GraphStore:
    """All graph operations backed by MongoDB."""

    def __init__(self):
        self._datasets_col, self._nodes_col, self._edges_col = collections()
        self._seed_if_empty()

    # ── Seed ─────────────────────────────────────────────────────────────────
    def _seed_if_empty(self):
        for key, ds in SEED_DATASETS.items():
            if self._datasets_col.find_one({"key": key}):
                continue  # already seeded

            # Insert dataset metadata
            self._datasets_col.insert_one({
                "key":         key,
                "name":        ds["name"],
                "description": ds.get("description", ""),
                "created_at":  _utc(),
            })

            # Insert nodes
            for n in ds["nodes"]:
                self._nodes_col.update_one(
                    {"dataset": key, "id": n["id"]},
                    {"$setOnInsert": {"dataset": key, **n, "created_at": _utc()}},
                    upsert=True,
                )

            # Insert edges
            for e in ds["edges"]:
                self._edges_col.update_one(
                    {"dataset": key, "id": e["id"]},
                    {"$setOnInsert": {"dataset": key, **e, "created_at": _utc()}},
                    upsert=True,
                )

            print(f"[GraphStore] Seeded dataset '{key}' → "
                  f"{len(ds['nodes'])} nodes, {len(ds['edges'])} edges")

    # ── Dataset ops ──────────────────────────────────────────────────────────
    def list_datasets(self) -> list[dict]:
        result = []
        for ds in self._datasets_col.find({}, {"_id": 0}):
            key = ds["key"]
            result.append({
                **ds,
                "node_count": self._nodes_col.count_documents({"dataset": key}),
                "edge_count": self._edges_col.count_documents({"dataset": key}),
                "labels": self._nodes_col.distinct("label", {"dataset": key}),
            })
        return result

    def get_dataset(self, key: str) -> dict | None:
        if not self._datasets_col.find_one({"key": key}):
            return None
        nodes = [_strip_mongo(n) for n in self._nodes_col.find({"dataset": key}, {"_id": 0})]
        edges = [_strip_mongo(e) for e in self._edges_col.find({"dataset": key}, {"_id": 0})]
        return {"nodes": nodes, "edges": edges}

    def reset_dataset(self, key: str) -> bool:
        if key not in SEED_DATASETS:
            return False
        self._nodes_col.delete_many({"dataset": key})
        self._edges_col.delete_many({"dataset": key})
        ds = SEED_DATASETS[key]
        for n in ds["nodes"]:
            self._nodes_col.insert_one({"dataset": key, **n, "created_at": _utc()})
        for e in ds["edges"]:
            self._edges_col.insert_one({"dataset": key, **e, "created_at": _utc()})
        print(f"[GraphStore] Reset dataset '{key}'")
        return True

    # ── Node ops ─────────────────────────────────────────────────────────────
    def get_node(self, dataset: str, node_id: str) -> dict | None:
        doc = self._nodes_col.find_one({"dataset": dataset, "id": node_id}, {"_id": 0})
        return doc

    def create_node(self, dataset: str, label: str, name: str,
                    props: dict | None = None) -> dict:
        # Ensure dataset record exists
        self._datasets_col.update_one(
            {"key": dataset},
            {"$setOnInsert": {"key": dataset, "name": dataset, "created_at": _utc()}},
            upsert=True,
        )
        node_id = f"node_{uuid.uuid4().hex[:8]}"
        node = {
            "dataset":    dataset,
            "id":         node_id,
            "label":      label,
            "name":       name,
            "created_at": _utc(),
            **(props or {}),
        }
        self._nodes_col.insert_one(node)
        return _strip_mongo(node)

    def update_node(self, dataset: str, node_id: str, updates: dict) -> dict | None:
        updates["updated_at"] = _utc()
        result = self._nodes_col.find_one_and_update(
            {"dataset": dataset, "id": node_id},
            {"$set": updates},
            projection={"_id": 0},
            return_document=True,
        )
        return result

    def delete_node(self, dataset: str, node_id: str) -> bool:
        res = self._nodes_col.delete_one({"dataset": dataset, "id": node_id})
        if res.deleted_count == 0:
            return False
        # Cascade delete edges
        self._edges_col.delete_many({
            "dataset": dataset,
            "$or": [{"source": node_id}, {"target": node_id}],
        })
        return True

    # ── Edge ops ─────────────────────────────────────────────────────────────
    def create_edge(self, dataset: str, source: str, target: str,
                    rel_type: str, props: dict | None = None) -> dict | None:
        # Verify both nodes exist
        if not self._nodes_col.find_one({"dataset": dataset, "id": source}):
            return None
        if not self._nodes_col.find_one({"dataset": dataset, "id": target}):
            return None
        edge_id = f"edge_{uuid.uuid4().hex[:8]}"
        edge = {
            "dataset":    dataset,
            "id":         edge_id,
            "source":     source,
            "target":     target,
            "type":       rel_type,
            "created_at": _utc(),
            **(props or {}),
        }
        self._edges_col.insert_one(edge)
        return _strip_mongo(edge)

    def delete_edge(self, dataset: str, edge_id: str) -> bool:
        res = self._edges_col.delete_one({"dataset": dataset, "id": edge_id})
        return res.deleted_count > 0

    # ── Cypher-lite ──────────────────────────────────────────────────────────
    def run_cypher(self, dataset: str, query: str) -> dict:
        if not self._datasets_col.find_one({"key": dataset}):
            return {"nodes": [], "edges": [], "message": f"Dataset '{dataset}' not found"}

        q = query.strip()

        # ── MATCH (n) RETURN n ──────────────────────────────────────────────
        if re.match(r"^MATCH\s*\(n\)\s*RETURN\s*n\s*$", q, re.I):
            nodes = [_strip_mongo(n) for n in self._nodes_col.find({"dataset": dataset}, {"_id": 0})]
            edges = [_strip_mongo(e) for e in self._edges_col.find({"dataset": dataset}, {"_id": 0})]
            return {"nodes": nodes, "edges": edges, "message": f"{len(nodes)} nodes, {len(edges)} edges"}

        # ── MATCH (n) RETURN n LIMIT k ──────────────────────────────────────
        m = re.match(r"^MATCH\s*\(n\)\s*RETURN\s*n\s*LIMIT\s*(\d+)\s*$", q, re.I)
        if m:
            k = int(m.group(1))
            nodes = [_strip_mongo(n) for n in self._nodes_col.find({"dataset": dataset}, {"_id": 0}).limit(k)]
            return {"nodes": nodes, "edges": [], "message": f"{len(nodes)} nodes (limit {k})"}

        # ── MATCH (n:Label) RETURN n ─────────────────────────────────────────
        m = re.match(r"^MATCH\s*\(n:(\w+)\)\s*RETURN\s*n\s*$", q, re.I)
        if m:
            label = m.group(1)
            nodes = [_strip_mongo(n) for n in
                     self._nodes_col.find({"dataset": dataset, "label": {"$regex": f"^{label}$", "$options": "i"}}, {"_id": 0})]
            return {"nodes": nodes, "edges": [], "message": f"{len(nodes)} nodes with label :{label}"}

        # ── MATCH (n {name:"X"}) RETURN n ───────────────────────────────────
        m = re.match(r'^MATCH\s*\(n\s*\{name:\s*["\'](.+?)["\']\}\)\s*RETURN\s*n\s*$', q, re.I)
        if m:
            name = m.group(1)
            nodes = [_strip_mongo(n) for n in
                     self._nodes_col.find({"dataset": dataset, "name": {"$regex": name, "$options": "i"}}, {"_id": 0})]
            return {"nodes": nodes, "edges": [], "message": f"{len(nodes)} nodes matching name \"{name}\""}

        # ── MATCH (a)-[r]->(b) RETURN a,r,b ────────────────────────────────
        if re.match(r"^MATCH\s*\(a\)\s*-\[r\]->\s*\(b\)\s*RETURN\s*a,r,b\s*$", q, re.I):
            nodes = [_strip_mongo(n) for n in self._nodes_col.find({"dataset": dataset}, {"_id": 0})]
            edges = [_strip_mongo(e) for e in self._edges_col.find({"dataset": dataset}, {"_id": 0})]
            return {"nodes": nodes, "edges": edges, "message": f"{len(nodes)} nodes, {len(edges)} relationships"}

        # ── MATCH (a)-[r:TYPE]->(b) RETURN a,b ──────────────────────────────
        m = re.match(r"^MATCH\s*\(a\)\s*-\[r:(\w+)\]->\s*\(b\)\s*RETURN\s*a,b\s*$", q, re.I)
        if m:
            rel_type = m.group(1).upper()
            matched_edges = [_strip_mongo(e) for e in
                             self._edges_col.find({"dataset": dataset, "type": rel_type}, {"_id": 0})]
            ids = {nid for e in matched_edges for nid in (e["source"], e["target"])}
            nodes = [_strip_mongo(n) for n in
                     self._nodes_col.find({"dataset": dataset, "id": {"$in": list(ids)}}, {"_id": 0})]
            return {"nodes": nodes, "edges": matched_edges,
                    "message": f"{len(nodes)} nodes in {len(matched_edges)} [{rel_type}] relationships"}

        # ── MATCH (a:Label)-[r]->(b) RETURN a,b ─────────────────────────────
        m = re.match(r"^MATCH\s*\(a:(\w+)\)\s*-\[r\]->\s*\(b\)\s*RETURN\s*a,b\s*$", q, re.I)
        if m:
            label = m.group(1)
            src_nodes = list(self._nodes_col.find(
                {"dataset": dataset, "label": {"$regex": f"^{label}$", "$options": "i"}}, {"_id": 0}))
            src_ids = {n["id"] for n in src_nodes}
            matched_edges = [_strip_mongo(e) for e in
                             self._edges_col.find({"dataset": dataset, "source": {"$in": list(src_ids)}}, {"_id": 0})]
            tgt_ids = {e["target"] for e in matched_edges}
            tgt_nodes = [_strip_mongo(n) for n in
                         self._nodes_col.find({"dataset": dataset, "id": {"$in": list(tgt_ids)}}, {"_id": 0})]
            all_nodes = [_strip_mongo(n) for n in src_nodes] + tgt_nodes
            unique = list({n["id"]: n for n in all_nodes}.values())
            return {"nodes": unique, "edges": matched_edges,
                    "message": f"{len(unique)} nodes connected to :{label}"}

        # ── MATCH (n:Label)-[r:TYPE]->(b) RETURN n,b ────────────────────────
        m = re.match(r"^MATCH\s*\(n:(\w+)\)\s*-\[r:(\w+)\]->\s*\(b\)\s*RETURN\s*n,b\s*$", q, re.I)
        if m:
            label, rel_type = m.group(1), m.group(2).upper()
            src_nodes = list(self._nodes_col.find(
                {"dataset": dataset, "label": {"$regex": f"^{label}$", "$options": "i"}}, {"_id": 0}))
            src_ids = {n["id"] for n in src_nodes}
            matched_edges = [_strip_mongo(e) for e in
                             self._edges_col.find(
                                 {"dataset": dataset, "source": {"$in": list(src_ids)}, "type": rel_type}, {"_id": 0})]
            all_ids = {nid for e in matched_edges for nid in (e["source"], e["target"])}
            nodes = [_strip_mongo(n) for n in
                     self._nodes_col.find({"dataset": dataset, "id": {"$in": list(all_ids)}}, {"_id": 0})]
            return {"nodes": nodes, "edges": matched_edges,
                    "message": f"{len(nodes)} nodes via :{label}-[{rel_type}]->"}

        # ── COUNT ─────────────────────────────────────────────────────────────
        if re.match(r"^MATCH\s*\(n\)\s*RETURN\s*COUNT\s*\(n\)\s*$", q, re.I):
            count = self._nodes_col.count_documents({"dataset": dataset})
            return {"nodes": [], "edges": [], "message": f"COUNT(n) = {count}"}

        return {"nodes": [], "edges": [],
                "message": "⚠ Unrecognised pattern. Try: MATCH (n) RETURN n"}

    # ── BFS shortest path ─────────────────────────────────────────────────────
    def shortest_path(self, dataset: str, start_id: str, end_id: str) -> dict:
        if not self._datasets_col.find_one({"key": dataset}):
            return {"path": [], "nodes": [], "edges": [], "message": "Dataset not found"}

        # Build adjacency list from MongoDB
        all_edges = list(self._edges_col.find({"dataset": dataset}, {"_id": 0}))
        adj: dict[str, list[str]] = {}
        for e in all_edges:
            adj.setdefault(e["source"], []).append(e["target"])
            adj.setdefault(e["target"], []).append(e["source"])

        # BFS
        visited: dict[str, str | None] = {start_id: None}
        queue = [start_id]
        found = False
        while queue:
            curr = queue.pop(0)
            if curr == end_id:
                found = True
                break
            for nbr in adj.get(curr, []):
                if nbr not in visited:
                    visited[nbr] = curr
                    queue.append(nbr)

        if not found:
            src = self._nodes_col.find_one({"dataset": dataset, "id": start_id}, {"_id": 0})
            tgt = self._nodes_col.find_one({"dataset": dataset, "id": end_id},   {"_id": 0})
            s = src["name"] if src else start_id
            t = tgt["name"] if tgt else end_id
            return {"path": [], "nodes": [], "edges": [],
                    "message": f"No path found between '{s}' and '{t}'"}

        # Reconstruct path
        path_ids: list[str] = []
        n = end_id
        while n is not None:
            path_ids.insert(0, n)
            n = visited[n]

        path_nodes = [_strip_mongo(doc) for doc in
                      self._nodes_col.find({"dataset": dataset, "id": {"$in": path_ids}}, {"_id": 0})]
        # Preserve path order
        node_map = {n["id"]: n for n in path_nodes}
        path_nodes = [node_map[nid] for nid in path_ids if nid in node_map]

        # Collect edges along path
        path_edges = []
        for i in range(len(path_ids) - 1):
            edge = self._edges_col.find_one({
                "dataset": dataset,
                "$or": [
                    {"source": path_ids[i],   "target": path_ids[i+1]},
                    {"source": path_ids[i+1], "target": path_ids[i]},
                ]
            }, {"_id": 0})
            if edge:
                path_edges.append(_strip_mongo(edge))

        src_name = node_map.get(start_id, {}).get("name", start_id)
        tgt_name = node_map.get(end_id,   {}).get("name", end_id)
        return {
            "path":    path_ids,
            "nodes":   path_nodes,
            "edges":   path_edges,
            "message": f"Path: {src_name} → {tgt_name} ({len(path_ids)} hops)",
        }

    # ── Statistics ────────────────────────────────────────────────────────────
    def get_stats(self, dataset: str) -> dict:
        if not self._datasets_col.find_one({"key": dataset}):
            return {}

        node_count = self._nodes_col.count_documents({"dataset": dataset})
        edge_count = self._edges_col.count_documents({"dataset": dataset})

        # Label breakdown via aggregation
        label_pipeline = [
            {"$match": {"dataset": dataset}},
            {"$group": {"_id": "$label", "count": {"$sum": 1}}},
        ]
        label_counts = {doc["_id"]: doc["count"]
                        for doc in self._nodes_col.aggregate(label_pipeline)}

        # Relationship type breakdown
        rel_pipeline = [
            {"$match": {"dataset": dataset}},
            {"$group": {"_id": "$type", "count": {"$sum": 1}}},
        ]
        rel_counts = {doc["_id"]: doc["count"]
                      for doc in self._edges_col.aggregate(rel_pipeline)}

        # Degree calculation via aggregation
        degree_pipeline = [
            {"$match": {"dataset": dataset}},
            {"$project": {"nodes": ["$source", "$target"]}},
            {"$unwind": "$nodes"},
            {"$group": {"_id": "$nodes", "degree": {"$sum": 1}}},
            {"$sort": {"degree": -1}},
            {"$limit": 5},
        ]
        top_raw = list(self._edges_col.aggregate(degree_pipeline))
        top_ids = [doc["_id"] for doc in top_raw]
        deg_map = {doc["_id"]: doc["degree"] for doc in top_raw}

        top_nodes = []
        for doc in self._nodes_col.find({"dataset": dataset, "id": {"$in": top_ids}}, {"_id": 0}):
            top_nodes.append({"id": doc["id"], "name": doc["name"], "degree": deg_map.get(doc["id"], 0)})
        top_nodes.sort(key=lambda x: -x["degree"])

        return {
            "node_count":         node_count,
            "edge_count":         edge_count,
            "label_counts":       label_counts,
            "relationship_types": rel_counts,
            "top_connected":      top_nodes,
        }


# ── Singleton ─────────────────────────────────────────────────────────────────
store = GraphStore()
