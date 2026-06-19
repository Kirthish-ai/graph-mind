"""
GraphMind — Streamlit Frontend
Connects to FastAPI backend at http://localhost:8000
Run: streamlit run app.py
"""

import streamlit as st
import requests
import plotly.graph_objects as go
import math
import random
import json
from collections import deque

# ── Config ─────────────────────────────────────────────────────────────────────
API = "http://localhost:8000"

st.set_page_config(
    page_title="GraphMind",
    page_icon="🕸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme ──────────────────────────────────────────────────────────────────────
LABEL_COLORS = {
    "Person":       "#e53030",
    "Organization": "#ff6b6b",
    "Company":      "#ff6b6b",
    "Movie":        "#ff4444",
    "Location":     "#ff8c42",
    "Concept":      "#e53030",
    "Genre":        "#ff6b6b",
    "Product":      "#ff4444",
    "Science":      "#e53030",
    "default":      "#b08888",
}

def label_color(label: str) -> str:
    return LABEL_COLORS.get(label, LABEL_COLORS["default"])

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Global ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #0a0000 !important;
    color: #f5e6e6 !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0f0505 !important;
    border-right: 1px solid #2d1010 !important;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stRadio label {
    color: #b08888 !important;
    font-size: 12px !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #f5e6e6 !important;
}

/* ── Main area ── */
.main .block-container { padding-top: 1rem; padding-bottom: 1rem; }

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: #140808 !important;
    border: 1px solid #2d1010 !important;
    border-radius: 8px !important;
    padding: 16px !important;
}
[data-testid="metric-container"] label {
    color: #b08888 !important;
    font-size: 10px !important;
    letter-spacing: 0.1em !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #e53030 !important;
    font-size: 24px !important;
    font-weight: 700 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #e53030 !important;
    color: #000 !important;
    border: none !important;
    border-radius: 4px !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    letter-spacing: 0.08em !important;
    padding: 8px 20px !important;
    transition: background 0.15s !important;
}
.stButton > button:hover {
    background: #ff4444 !important;
    box-shadow: 0 0 16px rgba(229,48,48,0.4) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background: #140808 !important;
    border: 1px solid #2d1010 !important;
    border-radius: 4px !important;
    color: #f5e6e6 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #e53030 !important;
    box-shadow: 0 0 0 2px rgba(229,48,48,0.15) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0f0505 !important;
    border-bottom: 1px solid #2d1010 !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #5c3333 !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    padding: 10px 20px !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #e53030 !important;
    border-bottom: 2px solid #e53030 !important;
    background: transparent !important;
}

/* ── Expanders ── */
.streamlit-expanderHeader {
    background: #140808 !important;
    border: 1px solid #2d1010 !important;
    color: #f5e6e6 !important;
    font-weight: 600 !important;
    font-size: 12px !important;
}
.streamlit-expanderContent {
    background: #0f0505 !important;
    border: 1px solid #2d1010 !important;
    border-top: none !important;
}

/* ── DataFrames/tables ── */
.stDataFrame { background: #140808 !important; }
[data-testid="stTable"] { background: #140808 !important; }

/* ── Code blocks ── */
code, pre {
    background: #140808 !important;
    color: #e53030 !important;
    font-family: 'JetBrains Mono', monospace !important;
    border: 1px solid #2d1010 !important;
    border-radius: 4px !important;
}

/* ── Divider ── */
hr { border-color: #2d1010 !important; }

/* ── Success/Error/Warning ── */
.stSuccess { background: rgba(229,48,48,0.1) !important; border-color: #e53030 !important; }
.stError   { background: rgba(229,48,48,0.15) !important; border-color: #e53030 !important; }
.stInfo    { background: rgba(176,136,136,0.1) !important; border-color: #b08888 !important; }

/* ── Selectbox dropdown ── */
[data-testid="stSelectbox"] > div { background: #140808 !important; }

/* ── Radio ── */
.stRadio > div { gap: 8px !important; }
.stRadio > div > label { 
    background: #140808 !important;
    border: 1px solid #2d1010 !important;
    border-radius: 4px !important;
    padding: 6px 12px !important;
    color: #b08888 !important;
    font-size: 12px !important;
}

/* ── Plotly chart bg ── */
.js-plotly-plot .plotly { background: #0a0000 !important; }

/* ── Node badge ── */
.node-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.08em;
    margin: 2px;
}

/* ── Stat pill ── */
.stat-pill {
    display: inline-block;
    background: #140808;
    border: 1px solid #2d1010;
    border-radius: 6px;
    padding: 10px 16px;
    text-align: center;
    margin: 4px;
}
.stat-pill .val { font-size: 22px; font-weight: 800; color: #e53030; }
.stat-pill .lbl { font-size: 10px; color: #5c3333; letter-spacing: 0.12em; margin-top: 2px; }
</style>
""", unsafe_allow_html=True)


# ── API helpers ────────────────────────────────────────────────────────────────
def api_get(path: str, params: dict = None) -> dict | list | None:
    try:
        r = requests.get(f"{API}{path}", params=params, timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error("⚠ Cannot connect to backend. Start it with: `cd backend && bash start.sh`")
        return None
    except Exception as e:
        st.error(f"API error: {e}")
        return None


def api_post(path: str, data: dict) -> dict | None:
    try:
        r = requests.post(f"{API}{path}", json=data, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error("⚠ Cannot connect to backend.")
        return None
    except Exception as e:
        st.error(f"API error: {e}")
        return None


def api_delete(path: str) -> dict | None:
    try:
        r = requests.delete(f"{API}{path}", timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"API error: {e}")
        return None


def api_patch(path: str, data: dict) -> dict | None:
    try:
        r = requests.patch(f"{API}{path}", json=data, timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"API error: {e}")
        return None


# ── Graph layout (Fruchterman-Reingold simplified) ─────────────────────────────
def compute_layout(nodes: list[dict], edges: list[dict], width=900, height=580, iterations=80) -> dict:
    if not nodes:
        return {}
    ids = [n["id"] for n in nodes]
    pos = {nid: [random.uniform(50, width - 50), random.uniform(50, height - 50)] for nid in ids}

    k = math.sqrt((width * height) / max(len(ids), 1)) * 0.8
    for _ in range(iterations):
        disp = {nid: [0.0, 0.0] for nid in ids}
        # Repulsion
        for i, a in enumerate(ids):
            for b in ids[i+1:]:
                dx = pos[a][0] - pos[b][0]
                dy = pos[a][1] - pos[b][1]
                d  = max(math.hypot(dx, dy), 0.01)
                f  = k * k / d
                disp[a][0] += dx / d * f
                disp[a][1] += dy / d * f
                disp[b][0] -= dx / d * f
                disp[b][1] -= dy / d * f
        # Attraction
        for e in edges:
            if e["source"] not in pos or e["target"] not in pos:
                continue
            dx = pos[e["source"]][0] - pos[e["target"]][0]
            dy = pos[e["source"]][1] - pos[e["target"]][1]
            d  = max(math.hypot(dx, dy), 0.01)
            f  = d * d / k
            disp[e["source"]][0] -= dx / d * f
            disp[e["source"]][1] -= dy / d * f
            disp[e["target"]][0] += dx / d * f
            disp[e["target"]][1] += dy / d * f
        # Update
        for nid in ids:
            dd = math.hypot(*disp[nid])
            if dd > 0:
                t = min(dd, k * 0.3)
                pos[nid][0] += disp[nid][0] / dd * t
                pos[nid][1] += disp[nid][1] / dd * t
                pos[nid][0] = max(30, min(width - 30,  pos[nid][0]))
                pos[nid][1] = max(30, min(height - 30, pos[nid][1]))
    return pos


# ── Graph figure builder ────────────────────────────────────────────────────────
def build_graph_figure(nodes, edges, highlight_ids=None, path_ids=None,
                       width=900, height=580) -> go.Figure:
    highlight_ids = set(highlight_ids or [])
    path_ids      = list(path_ids or [])
    path_set      = set(path_ids)
    path_edges    = set()
    for i in range(len(path_ids) - 1):
        path_edges.add((path_ids[i], path_ids[i+1]))
        path_edges.add((path_ids[i+1], path_ids[i]))

    pos = compute_layout(nodes, edges, width, height)

    fig = go.Figure()
    fig.update_layout(
        paper_bgcolor="#0a0000", plot_bgcolor="#0a0000",
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, width]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, height]),
        width=width, height=height,
        hovermode="closest",
        dragmode="pan",
    )

    # Draw edges
    for e in edges:
        src, tgt = e.get("source"), e.get("target")
        if src not in pos or tgt not in pos:
            continue
        is_path_edge = (src, tgt) in path_edges
        color = "#e53030" if is_path_edge else "#2d1010"
        width_val = 2.5 if is_path_edge else 1
        x0, y0 = pos[src]
        x1, y1 = pos[tgt]
        fig.add_trace(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            mode="lines",
            line=dict(color=color, width=width_val),
            hoverinfo="skip",
        ))
        # Edge label at midpoint
        mx, my = (x0+x1)/2, (y0+y1)/2
        fig.add_annotation(
            x=mx, y=my,
            text=f"<span style='font-size:9px;color:#5c3333;font-family:JetBrains Mono'>{e.get('type','')}</span>",
            showarrow=False,
            bgcolor="rgba(10,0,0,0.7)",
            bordercolor="#2d1010",
            borderwidth=1,
        )

    # Draw nodes
    for n in nodes:
        nid = n["id"]
        if nid not in pos:
            continue
        x, y = pos[nid]
        color = label_color(n.get("label", ""))
        is_path    = nid in path_set
        is_hilite  = nid in highlight_ids
        size = 28 if is_path else (22 if is_hilite else 18)
        border_color = "#ffffff" if is_path else (color if is_hilite else color)
        border_width = 3 if is_path else (2 if is_hilite else 1.5)
        fill = color if is_path else "#0a0000"

        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode="markers+text",
            marker=dict(
                size=size,
                color=fill,
                line=dict(color=border_color, width=border_width),
                symbol="circle",
            ),
            text=[n.get("name", nid)[:10]],
            textfont=dict(
                size=9,
                color="#ffffff" if is_path else "#f5e6e6",
                family="Inter",
            ),
            textposition="middle center",
            hovertext=f"<b>{n.get('name','')}</b><br>Label: {n.get('label','')}<br>ID: {nid}<br>{n.get('desc','')}",
            hoverinfo="text",
            name=n.get("name", nid),
            customdata=[nid],
        ))

    return fig


# ── BFS (client-side fallback) ─────────────────────────────────────────────────
def bfs_path(nodes, edges, start_id, end_id):
    adj = {n["id"]: [] for n in nodes}
    for e in edges:
        adj.get(e["source"], [None]).append(e["target"]) if e["source"] in adj else None
        adj.get(e["target"], [None]).append(e["source"]) if e["target"] in adj else None
    visited = {start_id: None}
    q = deque([start_id])
    while q:
        curr = q.popleft()
        if curr == end_id:
            break
        for nbr in adj.get(curr, []):
            if nbr not in visited:
                visited[nbr] = curr
                q.append(nbr)
    if end_id not in visited:
        return []
    path, n = [], end_id
    while n is not None:
        path.insert(0, n)
        n = visited[n]
    return path


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo
    st.markdown("""
    <div style='display:flex;align-items:center;gap:10px;margin-bottom:8px;'>
        <span style='font-size:22px;color:#e53030'>⬡</span>
        <span style='font-size:20px;font-weight:800;color:#f5e6e6'>Graph<span style='font-weight:300;color:#b08888'>Mind</span></span>
    </div>
    <div style='font-size:9px;font-weight:700;letter-spacing:.15em;color:#e53030;
                border:1px solid rgba(229,48,48,.3);border-radius:4px;
                padding:3px 8px;display:inline-block;margin-bottom:20px;
                background:rgba(229,48,48,.06)'>
        KNOWLEDGE GRAPH STUDIO
    </div>
    """, unsafe_allow_html=True)

    # ── Dataset picker ──
    st.markdown("#### DATASET")
    datasets_resp = api_get("/datasets")
    dataset_keys  = []
    dataset_meta  = {}
    if datasets_resp:
        for d in datasets_resp.get("datasets", []):
            dataset_keys.append(d["key"])
            dataset_meta[d["key"]] = d

    if not dataset_keys:
        dataset_keys = ["movies", "tech", "science", "graphmind"]

    if "selected_dataset" not in st.session_state:
        st.session_state.selected_dataset = "movies"

    for key in dataset_keys:
        meta  = dataset_meta.get(key, {})
        label = meta.get("name", key)
        n_cnt = meta.get("node_count", "–")
        e_cnt = meta.get("edge_count", "–")
        active = st.session_state.selected_dataset == key
        btn_style = "background:#1c0a0a;border:1px solid #e53030" if active else "background:#140808;border:1px solid #2d1010"
        txt_color = "#e53030" if active else "#b08888"
        if st.button(f"{'▶ ' if active else ''}{label}  ({n_cnt}N · {e_cnt}E)", key=f"ds_{key}",
                     use_container_width=True):
            st.session_state.selected_dataset = key
            st.session_state.pop("graph_data", None)
            st.rerun()

    st.markdown("---")

    # ── Reset dataset ──
    if st.button("↺  Reset to seed data", use_container_width=True):
        r = api_post(f"/datasets/{st.session_state.selected_dataset}/reset", {})
        if r:
            st.success(r.get("message", "Reset done"))
            st.session_state.pop("graph_data", None)
            st.rerun()

    st.markdown("---")

    # ── Live stats ──
    st.markdown("#### STATISTICS")
    stats = api_get(f"/datasets/{st.session_state.selected_dataset}/stats")
    if stats:
        st.metric("Nodes",  stats.get("node_count", 0))
        st.metric("Edges",  stats.get("edge_count", 0))
        st.metric("Labels", len(stats.get("label_counts", {})))

        st.markdown("**Top Connected**")
        for n in stats.get("top_connected", []):
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;padding:4px 0;"
                f"border-bottom:1px solid #2d1010;font-size:11px'>"
                f"<span style='color:#f5e6e6'>{n['name']}</span>"
                f"<span style='color:#e53030;font-family:JetBrains Mono'>{n['degree']}</span></div>",
                unsafe_allow_html=True
            )

    st.markdown("---")

    # ── Quick queries ──
    st.markdown("#### QUICK QUERIES")
    quick_queries = [
        "MATCH (n) RETURN n",
        "MATCH (n:Person) RETURN n",
        "MATCH (a)-[r]->(b) RETURN a,r,b",
        "MATCH (n:Organization) RETURN n",
        "MATCH (a)-[r:FOUNDED]->(b) RETURN a,b",
        "MATCH (n) RETURN COUNT(n)",
    ]
    for q in quick_queries:
        if st.button(q, key=f"qq_{q}", use_container_width=True):
            st.session_state.cypher_query = q
            st.session_state.active_tab   = "cypher"
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  LOAD GRAPH DATA
# ══════════════════════════════════════════════════════════════════════════════
if "graph_data" not in st.session_state:
    data = api_get(f"/datasets/{st.session_state.selected_dataset}")
    if data:
        st.session_state.graph_data = data
    else:
        st.session_state.graph_data = {"nodes": [], "edges": []}

graph_nodes = st.session_state.graph_data.get("nodes", [])
graph_edges = st.session_state.graph_data.get("edges", [])


# ══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════════
meta  = dataset_meta.get(st.session_state.selected_dataset, {})
dname = meta.get("name", st.session_state.selected_dataset)
ddesc = meta.get("description", "")

st.markdown(f"""
<div style='display:flex;align-items:baseline;gap:16px;margin-bottom:4px'>
    <h1 style='font-size:26px;font-weight:800;color:#f5e6e6;margin:0'>{dname}</h1>
    <span style='font-size:11px;font-weight:700;letter-spacing:.12em;color:#e53030;
                 background:rgba(229,48,48,.08);border:1px solid rgba(229,48,48,.3);
                 padding:2px 8px;border-radius:4px'>LIVE</span>
</div>
<p style='color:#5c3333;font-size:13px;margin-bottom:16px'>{ddesc}</p>
""", unsafe_allow_html=True)

# ── Top metrics bar ──
if stats:
    cols = st.columns(6)
    labels_data = stats.get("label_counts", {})
    all_metrics = [
        ("Nodes",  stats.get("node_count", 0)),
        ("Edges",  stats.get("edge_count", 0)),
        ("Labels", len(labels_data)),
        ("Rel Types", len(stats.get("relationship_types", {}))),
    ]
    for i, (lbl, val) in enumerate(all_metrics):
        cols[i].metric(lbl, val)

st.markdown("---")


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_graph, tab_cypher, tab_path, tab_nodes, tab_extract, tab_solutions = st.tabs([
    "🕸  GRAPH",
    "⌨  CYPHER",
    "📍 PATH",
    "🗄  NODES",
    "✨ EXTRACT",
    "📖 SOLUTIONS",
])


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — GRAPH VISUALISATION
# ══════════════════════════════════════════════════════════════════════════════
with tab_graph:
    col_graph, col_inspector = st.columns([3, 1])

    with col_graph:
        # Label filter
        all_labels = list({n.get("label", "?") for n in graph_nodes})
        if all_labels:
            selected_labels = st.multiselect(
                "Filter labels", all_labels, default=all_labels,
                label_visibility="collapsed",
                placeholder="Filter by label…",
                key="label_filter",
            )
            vis_nodes = [n for n in graph_nodes if n.get("label") in selected_labels]
            vis_node_ids = {n["id"] for n in vis_nodes}
            vis_edges = [e for e in graph_edges
                         if e.get("source") in vis_node_ids and e.get("target") in vis_node_ids]
        else:
            vis_nodes, vis_edges = graph_nodes, graph_edges

        # Search highlight
        search_q = st.text_input("", placeholder="🔍  Search nodes…", key="graph_search",
                                 label_visibility="collapsed")
        highlight = [n["id"] for n in vis_nodes
                     if search_q.lower() in n.get("name","").lower()] if search_q else []

        if vis_nodes:
            fig = build_graph_figure(vis_nodes, vis_edges, highlight_ids=highlight)
            st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True, "displayModeBar": False})
        else:
            st.info("No nodes to display. Adjust the label filter.")

    with col_inspector:
        st.markdown("#### NODE INSPECTOR")
        node_names = {n["name"]: n["id"] for n in graph_nodes}
        selected_name = st.selectbox("Select a node", ["— click to inspect —"] + list(node_names.keys()),
                                     label_visibility="collapsed")
        if selected_name != "— click to inspect —":
            nid = node_names[selected_name]
            node_detail = api_get(f"/datasets/{st.session_state.selected_dataset}/nodes/{nid}")
            if node_detail:
                n = node_detail["node"]
                color = label_color(n.get("label",""))
                st.markdown(f"""
                <div style='display:flex;align-items:center;gap:10px;padding:12px;
                            background:#140808;border:1px solid #2d1010;border-radius:6px;margin-bottom:8px'>
                    <div style='width:14px;height:14px;border-radius:50%;background:{color};flex-shrink:0'></div>
                    <div>
                        <div style='font-size:15px;font-weight:700;color:#f5e6e6'>{n.get('name','')}</div>
                        <div style='font-size:10px;color:#5c3333;letter-spacing:.08em'>{n.get('label','').upper()}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("**Properties**")
                skip = {"_id", "dataset"}
                for k, v in n.items():
                    if k in skip:
                        continue
                    st.markdown(
                        f"<div style='display:flex;justify-content:space-between;padding:4px 8px;"
                        f"background:#140808;border:1px solid #2d1010;border-radius:4px;margin-bottom:4px;font-size:12px'>"
                        f"<span style='color:#b08888'>{k}</span>"
                        f"<span style='color:#e53030;font-family:JetBrains Mono;font-size:11px'>{v}</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )

                out_edges = node_detail.get("outgoing", [])
                in_edges  = node_detail.get("incoming", [])
                if out_edges or in_edges:
                    st.markdown("**Relationships**")
                    nmap = {n["id"]: n["name"] for n in graph_nodes}
                    for e in out_edges:
                        tgt_name = nmap.get(e["target"], e["target"])
                        st.markdown(
                            f"<div style='font-size:11px;padding:4px 8px;background:#140808;"
                            f"border:1px solid #2d1010;border-radius:4px;margin-bottom:3px'>"
                            f"<span style='color:#5c3333'>→ </span>"
                            f"<span style='color:#e53030;font-family:JetBrains Mono'>[{e['type']}]</span> "
                            f"<span style='color:#b08888'>{tgt_name}</span></div>",
                            unsafe_allow_html=True
                        )
                    for e in in_edges:
                        src_name = nmap.get(e["source"], e["source"])
                        st.markdown(
                            f"<div style='font-size:11px;padding:4px 8px;background:#140808;"
                            f"border:1px solid #2d1010;border-radius:4px;margin-bottom:3px'>"
                            f"<span style='color:#5c3333'>← </span>"
                            f"<span style='color:#e53030;font-family:JetBrains Mono'>[{e['type']}]</span> "
                            f"<span style='color:#b08888'>{src_name}</span></div>",
                            unsafe_allow_html=True
                        )


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — CYPHER EDITOR
# ══════════════════════════════════════════════════════════════════════════════
with tab_cypher:
    col_editor, col_results = st.columns([1, 1])

    with col_editor:
        st.markdown("##### CYPHER EDITOR")
        default_q = st.session_state.get("cypher_query", "MATCH (n) RETURN n")
        query = st.text_area("", value=default_q, height=160,
                             placeholder="MATCH (n) RETURN n",
                             label_visibility="collapsed", key="cypher_input")

        c1, c2 = st.columns(2)
        run_btn   = c1.button("▶  RUN QUERY",   use_container_width=True, key="run_cypher")
        clear_btn = c2.button("✕  CLEAR",        use_container_width=True, key="clear_cypher")

        if clear_btn:
            st.session_state.cypher_query = "MATCH (n) RETURN n"
            st.session_state.pop("cypher_result", None)
            st.rerun()

        st.markdown("##### SYNTAX GUIDE")
        hints = [
            ("MATCH (n) RETURN n",                      "All nodes"),
            ("MATCH (n) RETURN n LIMIT 5",              "First 5 nodes"),
            ("MATCH (n:Person) RETURN n",               "By label"),
            ("MATCH (n {name:\"Alice\"}) RETURN n",     "By name"),
            ("MATCH (a)-[r]->(b) RETURN a,r,b",        "All with edges"),
            ("MATCH (a)-[r:FOUNDED]->(b) RETURN a,b",  "By rel type"),
            ("MATCH (a:Person)-[r]->(b) RETURN a,b",   "From label"),
            ("MATCH (n) RETURN COUNT(n)",               "Count nodes"),
        ]
        for h, desc in hints:
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;padding:5px 8px;"
                f"border-bottom:1px solid #2d1010;font-size:11px'>"
                f"<code style='background:none;border:none;color:#e53030;padding:0'>{h}</code>"
                f"<span style='color:#5c3333;flex-shrink:0;margin-left:8px'>{desc}</span></div>",
                unsafe_allow_html=True
            )

    with col_results:
        st.markdown("##### RESULTS")

        if run_btn and query.strip():
            result = api_post(f"/datasets/{st.session_state.selected_dataset}/cypher",
                              {"query": query.strip()})
            if result:
                st.session_state.cypher_result = result

        if "cypher_result" in st.session_state:
            res = st.session_state.cypher_result
            msg = res.get("message", "")
            res_nodes = res.get("nodes", [])
            res_edges = res.get("edges", [])

            st.success(f"✓  {msg}")

            if res_nodes:
                # Show graph
                fig2 = build_graph_figure(res_nodes, res_edges, width=480, height=320)
                st.plotly_chart(fig2, use_container_width=True,
                                config={"scrollZoom": True, "displayModeBar": False})

                # Node table
                st.markdown("**Matched Nodes**")
                for n in res_nodes:
                    color = label_color(n.get("label",""))
                    st.markdown(
                        f"<div style='display:flex;align-items:center;gap:8px;padding:6px 8px;"
                        f"background:#140808;border:1px solid #2d1010;border-radius:4px;margin-bottom:4px'>"
                        f"<div style='width:8px;height:8px;border-radius:50%;background:{color};flex-shrink:0'></div>"
                        f"<span style='font-size:12px;color:#f5e6e6;flex:1'>{n.get('name','')}</span>"
                        f"<span style='font-size:10px;color:#5c3333;font-family:JetBrains Mono'>{n.get('label','')}</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
            else:
                st.info("No nodes matched.")


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 3 — SHORTEST PATH
# ══════════════════════════════════════════════════════════════════════════════
with tab_path:
    st.markdown("##### SHORTEST PATH FINDER")
    st.markdown("<p style='color:#5c3333;font-size:13px'>BFS-based path tracing between any two nodes.</p>",
                unsafe_allow_html=True)

    node_name_list = [n["name"] for n in graph_nodes]
    node_id_by_name = {n["name"]: n["id"] for n in graph_nodes}

    c1, c2, c3 = st.columns([2, 2, 1])
    src_name = c1.selectbox("Source node",  node_name_list, key="path_src") if node_name_list else None
    tgt_name = c2.selectbox("Target node",  node_name_list, index=min(2, len(node_name_list)-1), key="path_tgt") if node_name_list else None
    find_btn = c3.button("FIND PATH", use_container_width=True, key="find_path")

    if find_btn and src_name and tgt_name and src_name != tgt_name:
        src_id = node_id_by_name[src_name]
        tgt_id = node_id_by_name[tgt_name]
        path_res = api_get(f"/datasets/{st.session_state.selected_dataset}/path",
                           params={"start": src_id, "end": tgt_id})
        if path_res:
            st.session_state.path_result = path_res

    if "path_result" in st.session_state:
        pr = st.session_state.path_result
        path_ids = pr.get("path", [])
        msg      = pr.get("message", "")

        if path_ids:
            st.success(f"✓  {msg}")

            # Full graph with path highlighted
            fig3 = build_graph_figure(graph_nodes, graph_edges, path_ids=path_ids, width=900, height=460)
            st.plotly_chart(fig3, use_container_width=True,
                            config={"scrollZoom": True, "displayModeBar": False})

            # Path breadcrumb
            nmap  = {n["id"]: n for n in graph_nodes}
            crumb = []
            for i, pid in enumerate(path_ids):
                n = nmap.get(pid, {})
                color = label_color(n.get("label",""))
                crumb.append(
                    f"<span style='display:inline-flex;align-items:center;gap:6px;"
                    f"background:#140808;border:1px solid #e53030;border-radius:4px;"
                    f"padding:4px 12px;font-size:12px;font-weight:600'>"
                    f"<span style='width:8px;height:8px;border-radius:50%;background:{color}'></span>"
                    f"{n.get('name',pid)}</span>"
                )
                if i < len(path_ids) - 1:
                    crumb.append("<span style='color:#e53030;font-size:18px;margin:0 4px'>→</span>")

            st.markdown(
                f"<div style='display:flex;align-items:center;flex-wrap:wrap;gap:4px;margin-top:12px'>"
                + "".join(crumb) + "</div>",
                unsafe_allow_html=True
            )
        else:
            st.error(f"✕  {msg}")


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 4 — NODE / EDGE MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════════
with tab_nodes:
    sub1, sub2, sub3 = st.tabs(["ADD NODE", "ADD EDGE", "DELETE"])

    # ── Add Node ──
    with sub1:
        st.markdown("##### ADD NEW NODE")
        with st.form("add_node_form"):
            n_name  = st.text_input("Entity Name", placeholder="e.g. Alice, Tesla, Berlin")
            n_label = st.selectbox("Label / Type",
                                   ["Person", "Organization", "Company", "Movie",
                                    "Location", "Concept", "Product", "Science", "Genre"])
            n_desc  = st.text_input("Description (optional)", placeholder="Short description")
            submitted = st.form_submit_button("ADD NODE", use_container_width=True)
            if submitted and n_name.strip():
                props = {"desc": n_desc} if n_desc else {}
                r = api_post(f"/datasets/{st.session_state.selected_dataset}/nodes",
                             {"label": n_label, "name": n_name.strip(), "props": props})
                if r:
                    st.success(f"✓ Node '{n_name}' added  (ID: {r['node']['id']})")
                    st.session_state.pop("graph_data", None)
                    st.rerun()

    # ── Add Edge ──
    with sub2:
        st.markdown("##### ADD NEW RELATIONSHIP")
        with st.form("add_edge_form"):
            nmap_form = {n["name"]: n["id"] for n in graph_nodes}
            node_opts = list(nmap_form.keys())
            e_src  = st.selectbox("Source Node",  node_opts, key="edge_src")
            e_tgt  = st.selectbox("Target Node",  node_opts, key="edge_tgt",
                                  index=min(1, len(node_opts)-1))
            e_type = st.text_input("Relationship Type",
                                   placeholder="e.g. FOUNDED, ACTED_IN, LOCATED_IN")
            e_submitted = st.form_submit_button("ADD EDGE", use_container_width=True)
            if e_submitted and e_type.strip() and e_src != e_tgt:
                r = api_post(f"/datasets/{st.session_state.selected_dataset}/edges", {
                    "source":   nmap_form[e_src],
                    "target":   nmap_form[e_tgt],
                    "rel_type": e_type.strip().upper(),
                    "props":    {},
                })
                if r:
                    st.success(f"✓ Edge [{e_type.upper()}] created  (ID: {r['edge']['id']})")
                    st.session_state.pop("graph_data", None)
                    st.rerun()

    # ── Delete ──
    with sub3:
        st.markdown("##### DELETE NODE OR EDGE")

        col_dn, col_de = st.columns(2)
        with col_dn:
            st.markdown("**Delete Node** *(cascades edges)*")
            del_node_opts = {n["name"]: n["id"] for n in graph_nodes}
            del_node_name = st.selectbox("Node to delete", ["— select —"] + list(del_node_opts.keys()),
                                         key="del_node_sel")
            if st.button("DELETE NODE", key="del_node_btn", use_container_width=True):
                if del_node_name != "— select —":
                    nid = del_node_opts[del_node_name]
                    r = api_delete(f"/datasets/{st.session_state.selected_dataset}/nodes/{nid}")
                    if r:
                        st.success(r.get("message","Deleted"))
                        st.session_state.pop("graph_data", None)
                        st.rerun()

        with col_de:
            st.markdown("**Delete Edge**")
            edge_opts = {f"[{e['type']}]  {e['source']} → {e['target']}": e["id"]
                         for e in graph_edges}
            del_edge_label = st.selectbox("Edge to delete", ["— select —"] + list(edge_opts.keys()),
                                          key="del_edge_sel")
            if st.button("DELETE EDGE", key="del_edge_btn", use_container_width=True):
                if del_edge_label != "— select —":
                    eid = edge_opts[del_edge_label]
                    r = api_delete(f"/datasets/{st.session_state.selected_dataset}/edges/{eid}")
                    if r:
                        st.success(r.get("message","Deleted"))
                        st.session_state.pop("graph_data", None)
                        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 5 — ENTITY EXTRACTION
# ══════════════════════════════════════════════════════════════════════════════
with tab_extract:
    st.markdown("##### ENTITY EXTRACTION")
    st.markdown("<p style='color:#5c3333;font-size:13px'>Paste any text — an article, biography, or paragraph. The engine extracts entities and relationships and saves them to the graph.</p>",
                unsafe_allow_html=True)

    col_in, col_out = st.columns([1, 1])

    with col_in:
        extract_text = st.text_area("", height=220,
            placeholder="Elon Musk founded Tesla and SpaceX. Tesla is headquartered in Austin, Texas. Sam Altman leads OpenAI which is located in San Francisco.",
            label_visibility="collapsed", key="extract_text_input")

        target_dataset = st.selectbox("Save to dataset",
                                      dataset_keys + ["custom"],
                                      index=dataset_keys.index(st.session_state.selected_dataset)
                                      if st.session_state.selected_dataset in dataset_keys else 0,
                                      key="extract_target_ds")
        save_toggle = st.checkbox("Save extracted entities to graph", value=True)
        extract_btn = st.button("✨  EXTRACT ENTITIES", use_container_width=True)

        # Preset examples
        st.markdown("**Try an example:**")
        examples = [
            "Elon Musk founded Tesla and SpaceX. Tesla is headquartered in Austin.",
            "Marie Curie discovered radioactivity and pioneered research in nuclear physics.",
            "Christopher Nolan directed Inception and Interstellar. Both films starred famous actors.",
            "Google acquired YouTube in 2006. Google is located in Silicon Valley.",
        ]
        for ex in examples:
            if st.button(ex[:60] + "…", key=f"ex_{ex[:20]}", use_container_width=True):
                st.session_state.extract_text_preset = ex
                st.rerun()

        if "extract_text_preset" in st.session_state:
            st.info(f"Preset loaded — click EXTRACT ENTITIES")

    with col_out:
        st.markdown("**Extraction Log**")

        use_text = st.session_state.get("extract_text_preset", extract_text) or extract_text

        if extract_btn and use_text.strip():
            st.session_state.pop("extract_text_preset", None)
            result = api_post("/extract", {
                "text":    use_text.strip(),
                "dataset": target_dataset,
                "save":    save_toggle,
            })
            if result:
                st.session_state.extract_result = result
                if save_toggle:
                    st.session_state.pop("graph_data", None)

        if "extract_result" in st.session_state:
            er = st.session_state.extract_result
            log    = er.get("log", [])
            nodes  = er.get("nodes", [])
            edges  = er.get("edges", [])
            saved  = er.get("saved_to", None)

            for line in log:
                if line.startswith("+"):
                    st.markdown(f"<div style='font-size:11px;color:#e53030;font-family:JetBrains Mono;"
                                f"padding:2px 0;border-bottom:1px solid #2d1010'>{line}</div>",
                                unsafe_allow_html=True)
                elif line.startswith("→"):
                    st.markdown(f"<div style='font-size:11px;color:#ff6b6b;font-family:JetBrains Mono;"
                                f"padding:2px 0;border-bottom:1px solid #2d1010'>{line}</div>",
                                unsafe_allow_html=True)
                elif line.startswith("✓"):
                    st.markdown(f"<div style='font-size:11px;color:#e53030;font-weight:700;padding:4px 0'>{line}</div>",
                                unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='font-size:11px;color:#5c3333;font-family:JetBrains Mono;"
                                f"padding:2px 0'>{line}</div>",
                                unsafe_allow_html=True)

            if saved:
                st.success(f"✓ Saved to dataset: **{saved}**")

            if nodes:
                st.markdown(f"**{len(nodes)} entities, {len(edges)} relationships extracted**")
                fig_ex = build_graph_figure(nodes, edges, width=460, height=260)
                st.plotly_chart(fig_ex, use_container_width=True,
                                config={"displayModeBar": False})


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 6 — SOLUTIONS (Q1–Q6)
# ══════════════════════════════════════════════════════════════════════════════
with tab_solutions:
    st.markdown("##### SYSTEM DESIGN SOLUTIONS — GraphMind Knowledge Graph Platform")

    solutions = {
        "Q1: Requirements Analysis": {
            "icon": "📋",
            "content": """
**Functional Requirements**
- **Multi-Source Ingestion:** Kafka CDC pipelines ingest structured (RDBMS, CSV), semi-structured (JSON, RDF), and unstructured text (PDFs, news) in near real-time.
- **Semantic Triple Extraction:** NLP models (spaCy + RoBERTa) extract Subject-Predicate-Object triples from raw text.
- **Entity Resolution:** SentenceTransformer cosine similarity merges duplicates (threshold > 0.92).
- **Graph CRUD:** ACID-compliant APIs for node/edge create, read, update, delete.
- **Hybrid Query Processing:** Single execution plan combining Cypher traversals + KNN vector search + scalar filters.
- **Graph Analytics:** Built-in PageRank, Louvain modularity, GraphSAGE for link prediction.

**Non-Functional Requirements**
- **Low Latency:** Sub-50ms for 3-hop traversals at any scale.
- **Horizontal Scalability:** Billions of nodes, trillions of edges across distributed shards.
- **High Availability:** 99.999% uptime surviving node crashes and network partitions.
- **Durability:** Write-ahead logging (WAL) + granular RBAC at node/edge property level.

**Why IFA beats RDBMS for traversal:**  
RDBMS needs nested JOINs → O(d^k) index lookups per hop. Index-Free Adjacency uses O(1) pointer dereferences — traversal speed independent of total graph size.
"""
        },
        "Q2: System Architecture": {
            "icon": "🏗",
            "content": """
**8-Layer Architecture (Top-Down)**

| Layer | Component | Technology |
|-------|-----------|-----------|
| 1 | API Gateway | gRPC + GraphQL/WebSocket + RBAC |
| 2 | Query Engine | Cypher/SPARQL + Cost-Based Optimizer |
| 3 | AI & Analytics | GraphSAGE, PageRank, Louvain |
| 4 | Semantic Indexer | HNSW vector index (Milvus) — <8ms KNN |
| 5 | Distributed Storage | RocksDB + Sharded IFA + Raft 3x replication |
| 6 | Entity Resolution | SentenceTransformers cosine similarity |
| 7 | NLP Pipeline | spaCy + RoBERTa — ~25ms/fragment |
| 8 | Ingestion | Kafka + Spark CDC — 500k writes/sec |

**Flow:** Raw data → Kafka → NLP → Entity Resolution → IFA write + HNSW update → Query Engine → API

**vs. Google KG:** Spanner/Paxos (global) vs. per-shard Raft → lower cross-DC latency  
**vs. Neo4j AuraDB:** Causal cluster Raft + GraphMind adds HNSW semantic layer  
**vs. Amazon Neptune:** Storage disaggregation principle shared; GraphMind extends with independent tier scaling
"""
        },
        "Q3: Construction Workflow": {
            "icon": "🔄",
            "content": """
**4-Step Pipeline**

1. **Ingest & Chunk** — Kafka CDC + sliding-window chunking preserves sentence boundaries
2. **NLP Extraction** — spaCy NER + RoBERTa extracts Subject-Predicate-Object triples (~25ms)
3. **Entity Resolution** — Embedding similarity check; merge if cosine > 0.92, else create new node
4. **Write & Index** — Commit to IFA shard + update HNSW vector index + Gossip sync replicas (<100ms lag)

**Hybrid Query Resolution:**
- User query semantically embedded → KNN search in HNSW → seed nodes in <8ms
- IFA pointer chain followed from seeds — O(1) per hop, no index scan
- Multi-shard traversals merged, returned as JSON sub-graph

**Pipeline Latency Budget:**

| Step | Time |
|------|------|
| NLP parsing | 24.5ms |
| Entity resolution | 8.2ms |
| Vector index write | 4.1ms |
| Graph DB commit | 1.8ms |
| **Total** | **38.6ms** ✓ |
"""
        },
        "Q4: Database Design": {
            "icon": "🗄",
            "content": """
**Property Graph Schema**

*Node Types:*
- `Person`: id (UUID), name, role, vector_embedding (float[1536])
- `Organization`: id, name, industry, revenue
- `Location`: id, name, country, lat_lon (Point2D)

*Edge Types:*
- `EMPLOYED_BY`: Person→Organization, since (Timestamp), salary
- `LOCATED_IN`: Org→Location, is_headquarters (Boolean)
- `INVESTED_IN`: Person/Org→Organization, amount (Double)

**Index-Free Adjacency Physical Layout:**
```
// nodes.db — fixed-size byte arrays
[NodeID 8B][TypeID 2B][FirstEdgePtr 8B][PropPtr 8B]

// edges.db
[EdgeID 8B][SrcPtr 8B][TgtPtr 8B][NextSrcEdgePtr 8B][NextTgtEdgePtr 8B]
```
Traversal: load node → read FirstEdgePtr → jump directly to edges.db offset → follow NextSrcEdgePtr chain. **O(1) per hop, size-independent.**

**Example Cypher Queries:**
```cypher
// Recommendation engine
MATCH (investor)-[:WORKS_AT]->(company)
MATCH (coworker)-[:WORKS_AT]->(company)
MATCH (coworker)-[i:INVESTED_IN]->(startup)
WHERE NOT (investor)-[:INVESTED_IN]->(startup)
RETURN startup.name, COUNT(coworker) DESC LIMIT 5

// Fraud ring detection
MATCH path=(acct)-[:TRANSFERRED_TO*3..5]->(acct)
RETURN path, length(path) AS CycleLength
```
"""
        },
        "Q5: Algorithm & Implementation": {
            "icon": "⚙",
            "content": """
**BFS — O(V+E)**
```python
from collections import deque

def breadth_first_search(graph, start):
    visited, queue, path = set(), deque([start]), []
    visited.add(start)
    while queue:
        node = queue.popleft()
        path.append(node)
        for edge in graph[node]['edges']:
            nbr = edge['target']
            if nbr not in visited:
                visited.add(nbr); queue.append(nbr)
    return path
```

**Dijkstra — O((V+E) log V)**
```python
import heapq

def dijkstra(graph, source, target):
    dist = {n: float('inf') for n in graph}
    prev = {n: None for n in graph}
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        cost, u = heapq.heappop(heap)
        if cost > dist[u]: continue
        if u == target: break
        for e in graph[u]['edges']:
            v, w = e['target'], e['weight']
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))
    path, node = [], target
    while node: path.append(node); node = prev[node]
    return list(reversed(path)), dist[target]
```

**Jaccard Recommendation — O(D_avg × V)**
```python
def jaccard(graph, a, b):
    na = {e['target'] for e in graph[a]['edges']}
    nb = {e['target'] for e in graph[b]['edges']}
    return len(na & nb) / len(na | nb) if (na | nb) else 0.0

def recommend(graph, node, top_n=3):
    direct = {e['target'] for e in graph[node]['edges']}
    scores = [(n, jaccard(graph, node, n))
              for n in graph if n != node and n not in direct]
    return sorted(scores, key=lambda x: -x[1])[:top_n]
```
"""
        },
        "Q6: Scalability & Fault Tolerance": {
            "icon": "⚡",
            "content": """
**Graph Partitioning Strategies**

| Strategy | Method | Best For |
|----------|--------|----------|
| Edge-Cut (METIS) | Group dense communities on one server | Sparse, community-structured graphs |
| Vertex-Cut | Replicate high-degree hubs across shards | Power-law topologies (social graphs) |

**Raft Consensus & Replication**
- Schema/metadata: Central Raft ring — majority quorum, strict serializability
- Data shards: 3-way synchronous replication per shard group
- Read replicas: Gossip protocol, eventual consistency <100ms

**Failure Handling**

| Scenario | Response |
|----------|----------|
| Follower crash | Leader continues 2/3 quorum; rejoiner replays WAL |
| Leader crash | New Raft election in 150-300ms; uncommitted entries rolled back |
| Network partition | Majority (2/3) stays operational; minority goes read-only |
| Traversal stale read | read-your-own-writes token routes to shard leader |

**Real-World Comparison**

| System | Consensus | Partitioning | Notes |
|--------|-----------|-------------|-------|
| **GraphMind** | Raft per-shard | METIS edge-cut + vertex-cut | + HNSW semantic layer |
| Google KG | Paxos (global) | Spanner tablets | Higher cross-DC latency |
| Neo4j AuraDB | Raft + Causal | Fabric sub-graphs | No native vector index |
| Amazon Neptune | Multi-AZ quorum | Storage striping | Disaggregated compute |
"""
        },
    }

    for title, sol in solutions.items():
        with st.expander(f"{sol['icon']}  {title}", expanded=False):
            st.markdown(sol["content"])


# ══════════════════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    "<div style='text-align:center;font-size:10px;color:#5c3333;letter-spacing:.12em;padding:8px'>"
    "GRAPHMIND · KNOWLEDGE GRAPH STUDIO · FastAPI + MongoDB + Streamlit"
    "</div>",
    unsafe_allow_html=True
)
