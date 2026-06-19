"""
entity_extractor.py — Rule-based entity and relationship extractor.
Parses natural language text into graph nodes and edges.
"""

import re
import uuid


# ── Relation patterns ─────────────────────────────────────────────────────────
PATTERNS = [
    (r"(\w[\w\s]+?)\s+(?:co-?)?founded\s+(\w[\w\s]+)",          "FOUNDED",          "Person",       "Organization"),
    (r"(\w[\w\s]+?)\s+(?:is\s+)?ceo\s+of\s+(\w[\w\s]+)",        "LEADS",            "Person",       "Organization"),
    (r"(\w[\w\s]+?)\s+leads?\s+(\w[\w\s]+)",                     "LEADS",            "Person",       "Organization"),
    (r"(\w[\w\s]+?)\s+acquired\s+(\w[\w\s]+)",                   "ACQUIRED",         "Organization", "Organization"),
    (r"(\w[\w\s]+?)\s+(?:bought|purchased)\s+(\w[\w\s]+)",       "ACQUIRED",         "Organization", "Organization"),
    (r"(\w[\w\s]+?)\s+works?\s+(?:at|for)\s+(\w[\w\s]+)",        "WORKS_AT",         "Person",       "Organization"),
    (r"(\w[\w\s]+?)\s+(?:is\s+)?employed\s+by\s+(\w[\w\s]+)",   "EMPLOYED_BY",      "Person",       "Organization"),
    (r"(\w[\w\s]+?)\s+(?:is\s+)?headquartered\s+in\s+(\w[\w\s]+)","HEADQUARTERED_IN","Organization", "Location"),
    (r"(\w[\w\s]+?)\s+(?:is\s+)?(?:located|based)\s+in\s+(\w[\w\s]+)", "LOCATED_IN","Organization", "Location"),
    (r"(\w[\w\s]+?)\s+launched\s+(\w[\w\s]+)",                   "LAUNCHED",         "Organization", "Product"),
    (r"(\w[\w\s]+?)\s+invented\s+(\w[\w\s]+)",                   "INVENTED",         "Person",       "Concept"),
    (r"(\w[\w\s]+?)\s+discovered\s+(\w[\w\s]+)",                 "DISCOVERED",       "Person",       "Concept"),
    (r"(\w[\w\s]+?)\s+developed\s+(\w[\w\s]+)",                  "DEVELOPED",        "Person",       "Concept"),
    (r"(\w[\w\s]+?)\s+proposed\s+(\w[\w\s]+)",                   "PROPOSED",         "Person",       "Concept"),
    (r"(\w[\w\s]+?)\s+invested\s+in\s+(\w[\w\s]+)",              "INVESTED_IN",      "Person",       "Organization"),
    (r"(\w[\w\s]+?)\s+partnered?\s+with\s+(\w[\w\s]+)",          "PARTNER_OF",       "Organization", "Organization"),
    (r"(\w[\w\s]+?)\s+collaborated?\s+with\s+(\w[\w\s]+)",       "COLLABORATED_WITH","Person",       "Person"),
    (r"(\w[\w\s]+?)\s+(?:is\s+)?part\s+of\s+(\w[\w\s]+)",       "PART_OF",          "Concept",      "Concept"),
    (r"(\w[\w\s]+?)\s+(?:is\s+a\s+)?product\s+of\s+(\w[\w\s]+)","PRODUCT_OF",       "Product",      "Organization"),
]

# Stop words to ignore as entity names
STOP_WORDS = {
    "the", "a", "an", "this", "that", "these", "those", "it", "its",
    "he", "she", "they", "we", "i", "you", "who", "which", "what",
    "and", "or", "but", "so", "yet", "for", "nor",
    "in", "on", "at", "to", "of", "by", "from", "with", "about",
    "also", "both", "each", "more", "most", "other", "some", "such",
    "than", "then", "too", "very", "just", "after", "before",
}


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip(" .,;:!?\"'()[]"))


def _valid(name: str) -> bool:
    name = name.strip()
    if len(name) < 2 or len(name) > 50:
        return False
    if name.lower() in STOP_WORDS:
        return False
    return True


def extract_entities(text: str) -> dict:
    """
    Parse text and return extracted nodes + edges.
    Returns:
        {
            "nodes": [...],
            "edges": [...],
            "log": [...]
        }
    """
    node_map: dict[str, dict] = {}   # name.lower() → node
    edges: list[dict] = []
    log: list[str] = []

    def get_or_create(name: str, label: str) -> dict | None:
        name = _clean(name)
        if not _valid(name):
            return None
        key = name.lower()
        if key not in node_map:
            nid = f"ex_{uuid.uuid4().hex[:8]}"
            node_map[key] = {
                "id": nid,
                "label": label,
                "name": name,
                "desc": f"Extracted {label.lower()}",
            }
            log.append(f"+ Node: {name} ({label})")
        return node_map[key]

    # Apply relation patterns
    for pattern, rel_type, src_label, tgt_label in PATTERNS:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            src_name = _clean(m.group(1))
            tgt_name = _clean(m.group(2))
            src = get_or_create(src_name, src_label)
            tgt = get_or_create(tgt_name, tgt_label)
            if src and tgt:
                # Avoid duplicate edges
                dup = any(
                    e["source"] == src["id"] and e["target"] == tgt["id"] and e["type"] == rel_type
                    for e in edges
                )
                if not dup:
                    edge = {
                        "id": f"ex_e_{uuid.uuid4().hex[:8]}",
                        "source": src["id"],
                        "target": tgt["id"],
                        "type": rel_type,
                    }
                    edges.append(edge)
                    log.append(f"→ Edge: ({src_name})-[{rel_type}]->({tgt_name})")

    # Fallback: extract capitalised proper nouns if nothing found
    if not node_map:
        log.append("› No patterns matched. Extracting proper nouns…")
        cap_matches = re.findall(r"\b([A-Z][a-z]+(?: [A-Z][a-z]+)*)\b", text)
        unique = list(dict.fromkeys(w for w in cap_matches if _valid(w)))[:12]
        labels = ["Person", "Organization", "Concept", "Location"]
        for i, word in enumerate(unique):
            label = labels[i % len(labels)]
            get_or_create(word, label)
        # Connect sequentially
        node_list = list(node_map.values())
        for i in range(1, len(node_list)):
            edge = {
                "id": f"ex_e_{uuid.uuid4().hex[:8]}",
                "source": node_list[i - 1]["id"],
                "target": node_list[i]["id"],
                "type": "RELATED_TO",
            }
            edges.append(edge)
            log.append(f"→ Edge: ({node_list[i-1]['name']})-[RELATED_TO]->({node_list[i]['name']})")

    nodes = list(node_map.values())
    log.insert(0, f"› Analysed text ({len(text)} chars)")
    log.append(f"✓ Done — {len(nodes)} entities, {len(edges)} relationships")

    return {"nodes": nodes, "edges": edges, "log": log}
