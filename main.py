"""
GraphMind Backend — FastAPI
Run: uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Any, Optional

from graph_store import store
from entity_extractor import extract_entities

# ── App ────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="GraphMind API",
    description="Knowledge graph backend — nodes, edges, Cypher queries, entity extraction",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow the local file:// frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response models ──────────────────────────────────────────────────
class NodeCreate(BaseModel):
    label: str
    name:  str
    props: dict[str, Any] = Field(default_factory=dict)

class NodeUpdate(BaseModel):
    props: dict[str, Any]

class EdgeCreate(BaseModel):
    source:   str
    target:   str
    rel_type: str
    props:    dict[str, Any] = Field(default_factory=dict)

class CypherQuery(BaseModel):
    query: str

class ExtractRequest(BaseModel):
    text:    str
    dataset: str = "custom"
    save:    bool = True    # whether to persist extracted nodes to the dataset


# ── Health ─────────────────────────────────────────────────────────────────────
@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "service": "GraphMind API", "version": "1.0.0"}

@app.get("/health", tags=["health"])
def health():
    return {"status": "healthy"}


# ── Datasets ───────────────────────────────────────────────────────────────────
@app.get("/datasets", tags=["datasets"])
def list_datasets():
    """List all available graph datasets."""
    return {"datasets": store.list_datasets()}


@app.get("/datasets/{dataset}", tags=["datasets"])
def get_dataset(dataset: str):
    """Get all nodes and edges for a dataset."""
    ds = store.get_dataset(dataset)
    if ds is None:
        raise HTTPException(status_code=404, detail=f"Dataset '{dataset}' not found")
    return ds


@app.post("/datasets/{dataset}/reset", tags=["datasets"])
def reset_dataset(dataset: str):
    """Reset a dataset to its seed data."""
    ok = store.reset_dataset(dataset)
    if not ok:
        raise HTTPException(status_code=404, detail=f"Dataset '{dataset}' not resettable")
    return {"message": f"Dataset '{dataset}' reset to seed data"}


# ── Stats ──────────────────────────────────────────────────────────────────────
@app.get("/datasets/{dataset}/stats", tags=["stats"])
def get_stats(dataset: str):
    """Get statistics for a dataset."""
    stats = store.get_stats(dataset)
    if not stats:
        raise HTTPException(status_code=404, detail=f"Dataset '{dataset}' not found")
    return stats


# ── Nodes ──────────────────────────────────────────────────────────────────────
@app.get("/datasets/{dataset}/nodes", tags=["nodes"])
def list_nodes(
    dataset: str,
    label: Optional[str] = Query(None, description="Filter by label"),
    search: Optional[str] = Query(None, description="Search by name"),
):
    """List nodes in a dataset, optionally filtered."""
    ds = store.get_dataset(dataset)
    if ds is None:
        raise HTTPException(status_code=404, detail=f"Dataset '{dataset}' not found")
    nodes = ds["nodes"]
    if label:
        nodes = [n for n in nodes if n["label"].lower() == label.lower()]
    if search:
        nodes = [n for n in nodes if search.lower() in n["name"].lower()]
    return {"nodes": nodes, "count": len(nodes)}


@app.get("/datasets/{dataset}/nodes/{node_id}", tags=["nodes"])
def get_node(dataset: str, node_id: str):
    """Get a single node with its relationships."""
    node = store.get_node(dataset, node_id)
    if node is None:
        raise HTTPException(status_code=404, detail=f"Node '{node_id}' not found")
    ds = store.get_dataset(dataset)
    edges = ds["edges"]
    outgoing = [e for e in edges if e["source"] == node_id]
    incoming = [e for e in edges if e["target"] == node_id]
    return {"node": node, "outgoing": outgoing, "incoming": incoming}


@app.post("/datasets/{dataset}/nodes", tags=["nodes"], status_code=201)
def create_node(dataset: str, body: NodeCreate):
    """Create a new node."""
    node = store.create_node(dataset, body.label, body.name, body.props)
    return {"node": node, "message": f"Node '{body.name}' created"}


@app.patch("/datasets/{dataset}/nodes/{node_id}", tags=["nodes"])
def update_node(dataset: str, node_id: str, body: NodeUpdate):
    """Update node properties."""
    node = store.update_node(dataset, node_id, body.props)
    if node is None:
        raise HTTPException(status_code=404, detail=f"Node '{node_id}' not found")
    return {"node": node, "message": "Node updated"}


@app.delete("/datasets/{dataset}/nodes/{node_id}", tags=["nodes"])
def delete_node(dataset: str, node_id: str):
    """Delete a node (and its edges)."""
    ok = store.delete_node(dataset, node_id)
    if not ok:
        raise HTTPException(status_code=404, detail=f"Node '{node_id}' not found")
    return {"message": f"Node '{node_id}' deleted (with its edges)"}


# ── Edges ──────────────────────────────────────────────────────────────────────
@app.post("/datasets/{dataset}/edges", tags=["edges"], status_code=201)
def create_edge(dataset: str, body: EdgeCreate):
    """Create a new relationship edge."""
    edge = store.create_edge(dataset, body.source, body.target, body.rel_type, body.props)
    if edge is None:
        raise HTTPException(status_code=400, detail="Source or target node not found")
    return {"edge": edge, "message": f"Edge [{body.rel_type}] created"}


@app.delete("/datasets/{dataset}/edges/{edge_id}", tags=["edges"])
def delete_edge(dataset: str, edge_id: str):
    """Delete a relationship edge."""
    ok = store.delete_edge(dataset, edge_id)
    if not ok:
        raise HTTPException(status_code=404, detail=f"Edge '{edge_id}' not found")
    return {"message": f"Edge '{edge_id}' deleted"}


# ── Cypher ─────────────────────────────────────────────────────────────────────
@app.post("/datasets/{dataset}/cypher", tags=["cypher"])
def run_cypher(dataset: str, body: CypherQuery):
    """
    Execute a Cypher-lite query against a dataset.

    Supported patterns:
    - MATCH (n) RETURN n
    - MATCH (n) RETURN n LIMIT k
    - MATCH (n:Label) RETURN n
    - MATCH (n {name:"X"}) RETURN n
    - MATCH (a)-[r]->(b) RETURN a,r,b
    - MATCH (a)-[r:TYPE]->(b) RETURN a,b
    - MATCH (a:Label)-[r]->(b) RETURN a,b
    - MATCH (n:Label)-[r:TYPE]->(b) RETURN n,b
    - MATCH (n) RETURN COUNT(n)
    """
    result = store.run_cypher(dataset, body.query)
    return result


# ── Shortest Path ──────────────────────────────────────────────────────────────
@app.get("/datasets/{dataset}/path", tags=["algorithms"])
def shortest_path(
    dataset: str,
    start: str = Query(..., description="Source node ID"),
    end:   str = Query(..., description="Target node ID"),
):
    """Find the BFS shortest path between two nodes."""
    result = store.shortest_path(dataset, start, end)
    return result


# ── Entity Extraction ──────────────────────────────────────────────────────────
@app.post("/extract", tags=["extract"])
def extract(body: ExtractRequest):
    """
    Extract entities and relationships from free text.
    Optionally saves them to a dataset.
    """
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    result = extract_entities(body.text)

    # Persist to dataset if requested
    if body.save and result["nodes"]:
        ds_key = body.dataset
        # Add extracted nodes
        id_map: dict[str, str] = {}   # extracted id → stored id
        for node in result["nodes"]:
            new_node = store.create_node(
                ds_key,
                node["label"],
                node["name"],
                {"desc": node.get("desc", ""), "source": "extraction"},
            )
            id_map[node["id"]] = new_node["id"]
            node["stored_id"] = new_node["id"]

        # Add extracted edges using mapped IDs
        for edge in result["edges"]:
            src_id = id_map.get(edge["source"], edge["source"])
            tgt_id = id_map.get(edge["target"], edge["target"])
            store.create_edge(ds_key, src_id, tgt_id, edge["type"])

        result["saved_to"] = ds_key
        result["node_count"] = len(result["nodes"])
        result["edge_count"] = len(result["edges"])

    return result


# ── Run directly ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
