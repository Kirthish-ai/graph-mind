/* ═══════════════════════════════════════════════════════════════
   GraphMind — Knowledge Graph Studio
   Main Application Controller
═══════════════════════════════════════════════════════════════ */

'use strict';

// ── Colour palette per node label ──────────────────────────────
const LABEL_COLORS = {
  Person:       '#00d4a0',
  Organization: '#4d9eff',
  Company:      '#4d9eff',
  Movie:        '#a78bfa',
  Location:     '#fb923c',
  Concept:      '#f472b6',
  Genre:        '#facc15',
  Product:      '#34d399',
  Science:      '#60a5fa',
  default:      '#94a3b8'
};

function labelColor(label) {
  return LABEL_COLORS[label] || LABEL_COLORS.default;
}

// ── Datasets ────────────────────────────────────────────────────
const DATASETS = {
  movies: {
    name: 'Movies & Actors',
    nodes: [
      { id: 'n1',  label: 'Movie',  name: 'The Matrix',       desc: '1999 sci-fi by the Wachowskis' },
      { id: 'n2',  label: 'Movie',  name: 'Inception',        desc: '2010 thriller by Christopher Nolan' },
      { id: 'n3',  label: 'Movie',  name: 'Interstellar',     desc: '2014 space epic by Christopher Nolan' },
      { id: 'n4',  label: 'Movie',  name: 'John Wick',        desc: '2014 action thriller' },
      { id: 'n5',  label: 'Movie',  name: 'Tenet',            desc: '2020 time-inversion thriller' },
      { id: 'n6',  label: 'Person', name: 'Keanu Reeves',     desc: 'Canadian actor' },
      { id: 'n7',  label: 'Person', name: 'Leonardo DiCaprio',desc: 'American actor and producer' },
      { id: 'n8',  label: 'Person', name: 'Christopher Nolan',desc: 'British-American director' },
      { id: 'n9',  label: 'Person', name: 'Lana Wachowski',   desc: 'American director' },
      { id: 'n10', label: 'Person', name: 'Matthew McConaughey', desc: 'American actor' },
      { id: 'n11', label: 'Person', name: 'John David Washington', desc: 'American actor' },
      { id: 'n12', label: 'Genre',  name: 'Sci-Fi',           desc: 'Science fiction genre' },
      { id: 'n13', label: 'Genre',  name: 'Action',           desc: 'Action genre' }
    ],
    edges: [
      { source: 'n6',  target: 'n1',  type: 'ACTED_IN' },
      { source: 'n9',  target: 'n1',  type: 'DIRECTED' },
      { source: 'n7',  target: 'n2',  type: 'ACTED_IN' },
      { source: 'n8',  target: 'n2',  type: 'DIRECTED' },
      { source: 'n8',  target: 'n3',  type: 'DIRECTED' },
      { source: 'n10', target: 'n3',  type: 'ACTED_IN' },
      { source: 'n8',  target: 'n5',  type: 'DIRECTED' },
      { source: 'n11', target: 'n5',  type: 'ACTED_IN' },
      { source: 'n6',  target: 'n4',  type: 'ACTED_IN' },
      { source: 'n1',  target: 'n12', type: 'IN_GENRE' },
      { source: 'n2',  target: 'n12', type: 'IN_GENRE' },
      { source: 'n3',  target: 'n12', type: 'IN_GENRE' },
      { source: 'n4',  target: 'n13', type: 'IN_GENRE' },
      { source: 'n5',  target: 'n12', type: 'IN_GENRE' }
    ]
  },

  tech: {
    name: 'Tech Companies',
    nodes: [
      { id: 't1',  label: 'Company',  name: 'Apple',       desc: 'Consumer electronics giant' },
      { id: 't2',  label: 'Company',  name: 'Tesla',       desc: 'Electric vehicles & energy' },
      { id: 't3',  label: 'Company',  name: 'SpaceX',      desc: 'Aerospace manufacturer' },
      { id: 't4',  label: 'Company',  name: 'OpenAI',      desc: 'AI research lab' },
      { id: 't5',  label: 'Company',  name: 'Google',      desc: 'Technology conglomerate' },
      { id: 't6',  label: 'Company',  name: 'Microsoft',   desc: 'Software & cloud giant' },
      { id: 't7',  label: 'Person',   name: 'Elon Musk',   desc: 'CEO of Tesla & SpaceX' },
      { id: 't8',  label: 'Person',   name: 'Steve Jobs',  desc: 'Co-founder of Apple' },
      { id: 't9',  label: 'Person',   name: 'Sam Altman',  desc: 'CEO of OpenAI' },
      { id: 't10', label: 'Person',   name: 'Sundar Pichai',desc: 'CEO of Google' },
      { id: 't11', label: 'Product',  name: 'iPhone',      desc: 'Smartphone by Apple' },
      { id: 't12', label: 'Product',  name: 'GPT-4',       desc: 'LLM by OpenAI' },
      { id: 't13', label: 'Location', name: 'Silicon Valley', desc: 'Tech hub in California' }
    ],
    edges: [
      { source: 't7',  target: 't2',  type: 'FOUNDED' },
      { source: 't7',  target: 't3',  type: 'FOUNDED' },
      { source: 't8',  target: 't1',  type: 'FOUNDED' },
      { source: 't9',  target: 't4',  type: 'LEADS' },
      { source: 't10', target: 't5',  type: 'LEADS' },
      { source: 't1',  target: 't11', type: 'MAKES' },
      { source: 't4',  target: 't12', type: 'CREATED' },
      { source: 't1',  target: 't13', type: 'LOCATED_IN' },
      { source: 't5',  target: 't13', type: 'LOCATED_IN' },
      { source: 't4',  target: 't13', type: 'LOCATED_IN' },
      { source: 't6',  target: 't4',  type: 'INVESTED_IN' },
      { source: 't5',  target: 't6',  type: 'COMPETES_WITH' }
    ]
  },

  science: {
    name: 'Scientific Minds',
    nodes: [
      { id: 's1',  label: 'Person',  name: 'Albert Einstein',   desc: 'Theoretical physicist' },
      { id: 's2',  label: 'Person',  name: 'Niels Bohr',        desc: 'Danish physicist' },
      { id: 's3',  label: 'Person',  name: 'Marie Curie',       desc: 'Polish-French physicist & chemist' },
      { id: 's4',  label: 'Person',  name: 'Isaac Newton',      desc: 'English mathematician & physicist' },
      { id: 's5',  label: 'Person',  name: 'Richard Feynman',   desc: 'American theoretical physicist' },
      { id: 's6',  label: 'Concept', name: 'Relativity',        desc: 'Einstein\'s theory of space-time' },
      { id: 's7',  label: 'Concept', name: 'Quantum Mechanics', desc: 'Physics of atomic scales' },
      { id: 's8',  label: 'Concept', name: 'Radioactivity',     desc: 'Spontaneous nuclear decay' },
      { id: 's9',  label: 'Concept', name: 'Gravity',           desc: 'Fundamental force' },
      { id: 's10', label: 'Concept', name: 'QED',               desc: 'Quantum electrodynamics' },
      { id: 's11', label: 'Science', name: 'Physics',           desc: 'Natural science' },
      { id: 's12', label: 'Science', name: 'Chemistry',         desc: 'Study of matter' }
    ],
    edges: [
      { source: 's1',  target: 's6',  type: 'PROPOSED' },
      { source: 's2',  target: 's7',  type: 'CONTRIBUTED_TO' },
      { source: 's1',  target: 's7',  type: 'CONTRIBUTED_TO' },
      { source: 's3',  target: 's8',  type: 'DISCOVERED' },
      { source: 's4',  target: 's9',  type: 'FORMULATED' },
      { source: 's5',  target: 's10', type: 'DEVELOPED' },
      { source: 's1',  target: 's11', type: 'STUDIED' },
      { source: 's2',  target: 's11', type: 'STUDIED' },
      { source: 's3',  target: 's12', type: 'STUDIED' },
      { source: 's6',  target: 's11', type: 'FIELD' },
      { source: 's7',  target: 's11', type: 'FIELD' },
      { source: 's1',  target: 's2',  type: 'COLLABORATED_WITH' }
    ]
  },

  graphmind: {
    name: 'GraphMind Schema',
    nodes: [
      { id: 'g1',  label: 'Concept',      name: 'GraphMind',         desc: 'Enterprise knowledge graph platform' },
      { id: 'g2',  label: 'Concept',      name: 'Index-Free Adj.',   desc: 'O(1) pointer-based traversal' },
      { id: 'g3',  label: 'Concept',      name: 'Raft Consensus',    desc: 'Distributed replication protocol' },
      { id: 'g4',  label: 'Concept',      name: 'HNSW Index',        desc: 'Hierarchical Navigable Small World' },
      { id: 'g5',  label: 'Concept',      name: 'Cypher Engine',     desc: 'Query language processor' },
      { id: 'g6',  label: 'Concept',      name: 'NLP Pipeline',      desc: 'Named entity recognition' },
      { id: 'g7',  label: 'Concept',      name: 'Vertex-Cut Part.', desc: 'Hub node replication strategy' },
      { id: 'g8',  label: 'Concept',      name: 'Entity Resolution', desc: 'Deduplication via embeddings' },
      { id: 'g9',  label: 'Organization', name: 'Neo4j',             desc: 'Graph database company' },
      { id: 'g10', label: 'Organization', name: 'Google',            desc: 'Knowledge Graph pioneer' },
      { id: 'g11', label: 'Product',      name: 'RocksDB',           desc: 'KV storage engine' },
      { id: 'g12', label: 'Product',      name: 'Apache Kafka',      desc: 'Distributed event streaming' }
    ],
    edges: [
      { source: 'g1',  target: 'g2',  type: 'USES' },
      { source: 'g1',  target: 'g3',  type: 'USES' },
      { source: 'g1',  target: 'g4',  type: 'USES' },
      { source: 'g1',  target: 'g5',  type: 'INCLUDES' },
      { source: 'g1',  target: 'g6',  type: 'INCLUDES' },
      { source: 'g1',  target: 'g7',  type: 'USES' },
      { source: 'g6',  target: 'g8',  type: 'FEEDS_INTO' },
      { source: 'g1',  target: 'g11', type: 'BUILT_ON' },
      { source: 'g1',  target: 'g12', type: 'BUILT_ON' },
      { source: 'g1',  target: 'g9',  type: 'INSPIRED_BY' },
      { source: 'g1',  target: 'g10', type: 'INSPIRED_BY' },
      { source: 'g9',  target: 'g2',  type: 'USES' }
    ]
  }
};

// ── Solution content ────────────────────────────────────────────
const SOLUTIONS = {
  q1: {
    title: 'Q1: Requirements Analysis',
    body: `
<h3>Functional Requirements</h3>
<ul>
  <li><strong>Multi-Source Ingestion:</strong> Ingest structured (RDBMS, CSV), semi-structured (JSON, RDF), and unstructured text (PDFs, news) in near real-time via Apache Kafka CDC pipelines.</li>
  <li><strong>Semantic Triple Extraction:</strong> NLP models identify entities (nodes) and relationships (edges), producing Subject-Predicate-Object triples from raw text.</li>
  <li><strong>Entity Resolution & Linking:</strong> Automatically merge duplicate entities using cosine similarity on vector embeddings (threshold &gt; 0.92).</li>
  <li><strong>Graph CRUD Operations:</strong> ACID-compliant APIs to add, update, and delete nodes, edges, and properties dynamically.</li>
  <li><strong>Hybrid Query Processing:</strong> Single execution plan combining Cypher path traversals, KNN vector similarity, and scalar filters.</li>
  <li><strong>Graph Analytics & Inference:</strong> Built-in PageRank, Louvain modularity, and GraphSAGE for node importance and link prediction.</li>
</ul>
<h3>Non-Functional Requirements</h3>
<ul>
  <li><strong>Low Traversal Latency:</strong> Sub-50ms response for 3-hop traversals at any graph scale.</li>
  <li><strong>Horizontal Scalability:</strong> Billions of nodes and trillions of edges across distributed shards.</li>
  <li><strong>High Availability:</strong> 99.999% uptime surviving isolated node crashes and network partitions.</li>
  <li><strong>Data Durability:</strong> Write-ahead logging (WAL) plus granular RBAC at the node/edge property level.</li>
</ul>
<h3>Why Relationship Modeling & Traversal Efficiency Matter</h3>
<p>RDBMS requires nested <code>JOIN</code> operations for multi-hop traversals — O(d^k) index lookups where d is degree and k is path depth. Index-Free Adjacency (IFA) replaces this with O(1) pointer dereferences, making traversal speed independent of total graph size.</p>
<h3>Why Scalability is Critical</h3>
<p>Global knowledge graphs (web, organizations, products) far exceed single-machine storage. Intelligent partitioning with METIS community detection minimises inter-server network hops during traversal.</p>
`
  },
  q2: {
    title: 'Q2: System Architecture Design',
    body: `
<h3>Architecture Layers (Top-Down)</h3>
<ul>
  <li><strong>API Gateway:</strong> gRPC (internal) + GraphQL/WebSocket (external). RBAC enforced at gateway level.</li>
  <li><strong>Query Coordination Engine:</strong> Receives Cypher/SPARQL, generates distributed execution plan via Cost-Based Optimizer (CBO). Routes sub-queries to shard leaders.</li>
  <li><strong>AI & Analytics Module:</strong> GraphSAGE, PageRank, Louvain Modularity on batch and micro-batch graph snapshots. Outputs centrality scores and link predictions.</li>
  <li><strong>Semantic Indexer:</strong> HNSW (Hierarchical Navigable Small World) vector index in Milvus. 1536-dim float vectors, KNN resolved in &lt;8ms.</li>
  <li><strong>Distributed Graph Storage:</strong> Sharded RocksDB KV engine storing IFA binary node/edge arrays. METIS edge-cut partitioning. 3-way synchronous Raft replication per shard.</li>
  <li><strong>Entity Resolution Layer:</strong> SentenceTransformers cosine similarity cache. Merges entities above 0.92 similarity threshold.</li>
  <li><strong>NLP Extraction Pipeline:</strong> spaCy + fine-tuned RoBERTa, ~25ms per fragment, outputs unresolved entity-relationship triples.</li>
  <li><strong>Data Ingestion Layer:</strong> Apache Kafka + Spark Streaming CDC. Handles 500,000 writes/sec.</li>
</ul>
<h3>Component Interaction Flow</h3>
<p>Raw data → Kafka → NLP extraction → Entity resolution → IFA storage write + HNSW vector index update → Query engine reads from both storage layers → AI analytics batch layer → API Gateway response.</p>
<h3>Comparison with Production Systems</h3>
<ul>
  <li><strong>Google KG:</strong> Uses Spanner (Paxos, global) vs GraphMind's per-shard Raft — lower cross-datacenter latency.</li>
  <li><strong>Neo4j AuraDB:</strong> Causal cluster Raft + read replicas. GraphMind adds HNSW semantic layer not native to Neo4j.</li>
  <li><strong>Amazon Neptune:</strong> Storage disaggregated from compute. GraphMind adopts same principle for independent scaling.</li>
</ul>
`
  },
  q3: {
    title: 'Q3: Graph Construction & Query Workflow',
    body: `
<h3>4-Step Construction Pipeline</h3>
<ul>
  <li><strong>1. Ingest & Chunk:</strong> Documents ingested via Kafka CDC. Sliding-window chunking preserves sentence boundaries for NLP accuracy.</li>
  <li><strong>2. NLP Extraction:</strong> spaCy NER + RoBERTa relationship classifier detects Subject-Predicate-Object triples from text chunks (~25ms each).</li>
  <li><strong>3. Entity Resolution:</strong> SentenceTransformer embeddings generated per entity. Cosine similarity against existing nodes — merge if score &gt; 0.92, else create new node.</li>
  <li><strong>4. Write & Index:</strong> Commit triple to IFA storage shard. Update HNSW vector index with new embeddings. Gossip protocol syncs read replicas (&lt;100ms lag).</li>
</ul>
<h3>Hybrid Query Resolution Flow</h3>
<ul>
  <li><strong>Seed node selection:</strong> User query semantically embedded → KNN search in HNSW → seed nodes identified in &lt;8ms.</li>
  <li><strong>Graph traversal:</strong> IFA pointer chain followed from seed nodes — O(1) per hop, no index scan.</li>
  <li><strong>Aggregation:</strong> Traversals across shards merged, returned as JSON sub-graph.</li>
</ul>
<h3>End-to-End Pipeline Latency Budget</h3>
<ul>
  <li>NLP text parsing: <strong>24.5ms</strong></li>
  <li>Entity resolution: <strong>8.2ms</strong></li>
  <li>Vector index write: <strong>4.1ms</strong></li>
  <li>Graph DB commit: <strong>1.8ms</strong></li>
  <li><strong>Total: 38.6ms</strong> — well within 50ms SLA.</li>
</ul>
`
  },
  q4: {
    title: 'Q4: Database Design',
    body: `
<h3>Property Graph Schema</h3>
<p>GraphMind uses a Property Graph Model where nodes and edges both carry arbitrary key-value properties — unlike RDF where properties require intermediate nodes.</p>
<h3>Node Types</h3>
<ul>
  <li><strong>Person:</strong> id (UUID), name (String), role (String), vector_embedding (float[1536])</li>
  <li><strong>Organization:</strong> id (UUID), name (String), industry (String), revenue (Double)</li>
  <li><strong>Location:</strong> id (UUID), name (String), country (String), lat_lon (Point2D)</li>
</ul>
<h3>Edge Types</h3>
<ul>
  <li><strong>EMPLOYED_BY:</strong> Person→Organization, since (Timestamp), salary (Decimal)</li>
  <li><strong>LOCATED_IN:</strong> Org/Location→Location, is_headquarters (Boolean)</li>
  <li><strong>INVESTED_IN:</strong> Person/Org→Organization, amount (Double)</li>
</ul>
<h3>Index-Free Adjacency Physical Layout</h3>
<p>Fixed-size byte arrays on disk. Each node record contains a direct memory pointer to its first edge record in edges.db. The engine follows the <code>Next Source Edge Pointer</code> chain — traversal is O(1) per hop, size-independent.</p>
<pre><code>// nodes.db
[NodeID 8B][TypeID 2B][FirstEdgePtr 8B][PropPtr 8B]

// edges.db  
[EdgeID 8B][SrcPtr 8B][TgtPtr 8B][NextSrcEdgePtr 8B][NextTgtEdgePtr 8B]</code></pre>
<h3>Cypher Query Examples</h3>
<pre><code>// Recommendation engine
MATCH (investor:Person)-[:WORKS_AT]->(company)
MATCH (coworker)-[:WORKS_AT]->(company)
MATCH (coworker)-[i:INVESTED_IN]->(startup)
WHERE NOT (investor)-[:INVESTED_IN]->(startup)
RETURN startup.name, COUNT(coworker)
ORDER BY COUNT(coworker) DESC LIMIT 5

// Fraud ring detection
MATCH path=(acct:BankAccount)-[:TRANSFERRED_TO*3..5]->(acct)
RETURN path, length(path) AS CycleLength</code></pre>
`
  },
  q5: {
    title: 'Q5: Algorithm & Implementation',
    body: `
<h3>BFS Traversal — O(V+E)</h3>
<pre><code>from collections import deque

def breadth_first_search(graph, start):
    visited, queue, path = set(), deque([start]), []
    visited.add(start)
    while queue:
        node = queue.popleft()
        path.append(node)
        for edge in graph[node]['edges']:
            nbr = edge['target']
            if nbr not in visited:
                visited.add(nbr)
                queue.append(nbr)
    return path</code></pre>
<h3>Dijkstra Shortest Path — O((V+E) log V)</h3>
<pre><code>import heapq

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
    # Reconstruct path
    path, node = [], target
    while node: path.append(node); node = prev[node]
    return list(reversed(path)), dist[target]</code></pre>
<h3>Jaccard Recommendation — O(D_avg × V)</h3>
<pre><code>def jaccard_similarity(graph, a, b):
    na = {e['target'] for e in graph[a]['edges']}
    nb = {e['target'] for e in graph[b]['edges']}
    inter = na & nb
    union = na | nb
    return len(inter) / len(union) if union else 0.0

def recommend(graph, node, top_n=3):
    direct = {e['target'] for e in graph[node]['edges']}
    scores = [
        (n, jaccard_similarity(graph, node, n))
        for n in graph if n != node and n not in direct
    ]
    scores.sort(key=lambda x: -x[1])
    return scores[:top_n]</code></pre>
<p>These algorithms are demonstrated live in the <strong>PATH mode</strong> on the graph canvas — click any two nodes to see BFS shortest path highlighted in teal.</p>
`
  },
  q6: {
    title: 'Q6: Scalability & Fault Tolerance',
    body: `
<h3>Horizontal Graph Partitioning</h3>
<p>Standard key-based sharding causes graph traversals to cross server boundaries — each hop becomes a network RPC. GraphMind uses two complementary strategies:</p>
<ul>
  <li><strong>Edge-Cut (METIS):</strong> Nodes grouped into dense communities on one server. Inter-community edges are cut. Optimal for sparse, community-structured graphs.</li>
  <li><strong>Vertex-Cut:</strong> High-degree hub nodes (e.g. "USA", "Google") replicated across shards. Edges stored locally. Optimal for power-law topologies.</li>
</ul>
<h3>Raft Consensus & Replication</h3>
<ul>
  <li><strong>Schema & metadata:</strong> Central Raft consensus ring. Writes require majority quorum — strict serializability.</li>
  <li><strong>Data shards:</strong> 3-way synchronous replication per shard group. Each shard has one leader, two followers.</li>
  <li><strong>Read replicas:</strong> Gossip protocol sync, eventual consistency within &lt;100ms of write confirmation.</li>
</ul>
<h3>Failure Scenarios</h3>
<ul>
  <li><strong>Follower crash:</strong> Leader continues with 2/3 quorum. Crashed follower rejoins by replaying WAL log from leader.</li>
  <li><strong>Leader crash:</strong> Raft elects new leader in ~150-300ms. Uncommitted entries rolled back.</li>
  <li><strong>Network partition:</strong> Majority partition (2/3) stays operational. Minority partition goes read-only, rejoins after healing via log replay.</li>
  <li><strong>Traversal inconsistency:</strong> Read-your-own-writes token routes reads to shard leader during lag window — prevents stale traversals.</li>
</ul>
<h3>Real-World Comparison</h3>
<ul>
  <li><strong>Google KG:</strong> Spanner + Paxos (global) → higher cross-DC latency than GraphMind's per-shard Raft.</li>
  <li><strong>Neo4j AuraDB:</strong> Causal cluster Raft + transaction IDs. GraphMind extends this with HNSW semantic layer.</li>
  <li><strong>Amazon Neptune:</strong> Multi-AZ quorum, disaggregated storage. GraphMind adopts storage disaggregation for independent tier scaling.</li>
</ul>
`
  }
};

/* ═══════════════════════════════════════════════════════════════
   GRAPH PHYSICS ENGINE
═══════════════════════════════════════════════════════════════ */
class GraphPhysics {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx    = canvas.getContext('2d');
    this.nodes  = [];
    this.edges  = [];
    this.zoom   = 1;
    this.panX   = 0;
    this.panY   = 0;
    this.dragging       = null;
    this.isPanning      = false;
    this.lastMouse      = { x: 0, y: 0 };
    this.hoveredNode    = null;
    this.selectedNode   = null;
    this.pathNodes      = [];   // highlighted path
    this.queryNodes     = [];   // highlighted query result nodes
    this.hiddenLabels   = new Set();
    this.animFrame      = null;
    this.onNodeClick    = null;
    this.onCanvasClick  = null;
    this.resize();
    this.bindEvents();
    this.tick();
  }

  resize() {
    const r = this.canvas.parentElement.getBoundingClientRect();
    this.canvas.width  = r.width;
    this.canvas.height = r.height;
  }

  /* ── Load dataset ── */
  loadDataset(ds) {
    this.nodes = ds.nodes.map(n => ({
      ...n,
      x: this.canvas.width  / 2 + (Math.random() - .5) * 300,
      y: this.canvas.height / 2 + (Math.random() - .5) * 300,
      vx: 0, vy: 0
    }));
    this.edges = ds.edges.map(e => ({ ...e }));
    this.selectedNode = null;
    this.pathNodes    = [];
    this.queryNodes   = [];
    this.resetView();
  }

  resetView() {
    this.zoom = 1; this.panX = 0; this.panY = 0;
  }

  /* ── Physics tick ── */
  tick() {
    this.update();
    this.draw();
    this.animFrame = requestAnimationFrame(() => this.tick());
  }

  update() {
    const nodes = this.nodes.filter(n => !this.hiddenLabels.has(n.label));
    const k = 80, repulse = 6000, dampen = 0.75, attract = 0.04;

    // Reset forces
    nodes.forEach(n => { n.fx = 0; n.fy = 0; });

    // Repulsion
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const a = nodes[i], b = nodes[j];
        const dx = b.x - a.x, dy = b.y - a.y;
        const dist = Math.max(Math.hypot(dx, dy), 1);
        const f = repulse / (dist * dist);
        const fx = (dx / dist) * f, fy = (dy / dist) * f;
        a.fx -= fx; a.fy -= fy;
        b.fx += fx; b.fy += fy;
      }
    }

    // Spring attraction for edges
    this.edges.forEach(e => {
      const src = this.nodes.find(n => n.id === e.source);
      const tgt = this.nodes.find(n => n.id === e.target);
      if (!src || !tgt) return;
      if (this.hiddenLabels.has(src.label) || this.hiddenLabels.has(tgt.label)) return;
      const dx = tgt.x - src.x, dy = tgt.y - src.y;
      const dist = Math.max(Math.hypot(dx, dy), 1);
      const f = (dist - k) * attract;
      const fx = (dx / dist) * f, fy = (dy / dist) * f;
      src.fx += fx; src.fy += fy;
      tgt.fx -= fx; tgt.fy -= fy;
    });

    // Centre gravity
    const cx = this.canvas.width / 2, cy = this.canvas.height / 2;
    nodes.forEach(n => {
      n.fx += (cx - n.x) * 0.004;
      n.fy += (cy - n.y) * 0.004;
    });

    // Integrate
    nodes.forEach(n => {
      if (this.dragging === n) return;
      n.vx = (n.vx + n.fx) * dampen;
      n.vy = (n.vy + n.fy) * dampen;
      n.x += n.vx;
      n.y += n.vy;
    });
  }

  draw() {
    const ctx = this.ctx;
    ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    ctx.save();

    // Apply pan/zoom from centre
    const cx = this.canvas.width / 2, cy = this.canvas.height / 2;
    ctx.translate(cx + this.panX, cy + this.panY);
    ctx.scale(this.zoom, this.zoom);
    ctx.translate(-cx, -cy);

    const visNodes = this.nodes.filter(n => !this.hiddenLabels.has(n.label));

    // Draw edges
    this.edges.forEach(e => {
      const src = visNodes.find(n => n.id === e.source);
      const tgt = visNodes.find(n => n.id === e.target);
      if (!src || !tgt) return;

      const isPath = this.pathNodes.length > 1 &&
        this.pathNodes.includes(src.id) && this.pathNodes.includes(tgt.id);

      ctx.beginPath();
      ctx.moveTo(src.x, src.y);
      ctx.lineTo(tgt.x, tgt.y);

      if (isPath) {
        ctx.strokeStyle = 'rgba(0,212,160,0.9)';
        ctx.lineWidth = 2.5 / this.zoom;
        ctx.shadowColor = '#00d4a0';
        ctx.shadowBlur = 8;
      } else {
        ctx.strokeStyle = 'rgba(30,45,68,0.9)';
        ctx.lineWidth = 1 / this.zoom;
        ctx.shadowBlur = 0;
      }
      ctx.stroke();
      ctx.shadowBlur = 0;

      // Edge label
      if (this.zoom > 0.7) {
        const mx = (src.x + tgt.x) / 2, my = (src.y + tgt.y) / 2;
        ctx.fillStyle = isPath ? 'rgba(0,212,160,0.9)' : 'rgba(74,85,104,0.8)';
        ctx.font = `${10 / this.zoom}px JetBrains Mono, monospace`;
        ctx.textAlign = 'center';
        ctx.fillText(e.type, mx, my - 4 / this.zoom);
      }

      // Arrow
      const angle = Math.atan2(tgt.y - src.y, tgt.x - src.x);
      const r = 18 / this.zoom;
      const ax = tgt.x - r * Math.cos(angle);
      const ay = tgt.y - r * Math.sin(angle);
      const as = 6 / this.zoom;
      ctx.fillStyle = isPath ? 'rgba(0,212,160,0.9)' : 'rgba(38,52,80,0.9)';
      ctx.beginPath();
      ctx.moveTo(ax, ay);
      ctx.lineTo(ax - as * Math.cos(angle - .4), ay - as * Math.sin(angle - .4));
      ctx.lineTo(ax - as * Math.cos(angle + .4), ay - as * Math.sin(angle + .4));
      ctx.closePath();
      ctx.fill();
    });

    // Draw nodes
    visNodes.forEach(n => {
      const r = 18 / this.zoom;
      const color = labelColor(n.label);
      const isSelected  = this.selectedNode?.id === n.id;
      const isPath      = this.pathNodes.includes(n.id);
      const isQuery     = this.queryNodes.includes(n.id);
      const isHovered   = this.hoveredNode?.id === n.id;

      // Glow
      if (isSelected || isPath || isQuery || isHovered) {
        ctx.beginPath();
        ctx.arc(n.x, n.y, r + 8 / this.zoom, 0, Math.PI * 2);
        ctx.fillStyle = isPath ? 'rgba(0,212,160,0.12)' : `${color}18`;
        ctx.fill();
        ctx.shadowColor = isPath ? '#00d4a0' : color;
        ctx.shadowBlur = 16;
      }

      // Circle
      ctx.beginPath();
      ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
      if (isSelected || isPath) {
        ctx.fillStyle = isPath ? '#00d4a0' : color;
        ctx.strokeStyle = '#fff';
      } else if (isQuery) {
        ctx.fillStyle = color;
        ctx.strokeStyle = '#fff';
      } else {
        ctx.fillStyle = '#0a0e1a';
        ctx.strokeStyle = color;
      }
      ctx.lineWidth = (isSelected || isPath) ? 2.5 / this.zoom : 1.5 / this.zoom;
      ctx.fill();
      ctx.stroke();
      ctx.shadowBlur = 0;

      // Label
      if (this.zoom > 0.45) {
        ctx.fillStyle = (isSelected || isPath) ? '#000' : '#e2e8f0';
        ctx.font = `bold ${9 / this.zoom}px Inter, sans-serif`;
        ctx.textAlign = 'center';
        const label = n.name.length > 10 ? n.name.slice(0, 9) + '…' : n.name;
        ctx.fillText(label, n.x, n.y + 3 / this.zoom);
      }
    });

    ctx.restore();
  }

  /* ── World ↔ Screen coords ── */
  screenToWorld(sx, sy) {
    const cx = this.canvas.width / 2, cy = this.canvas.height / 2;
    return {
      x: (sx - cx - this.panX) / this.zoom + cx,
      y: (sy - cy - this.panY) / this.zoom + cy
    };
  }

  getNodeAt(sx, sy) {
    const w = this.screenToWorld(sx, sy);
    const r = 20 / this.zoom;
    return this.nodes.find(n =>
      !this.hiddenLabels.has(n.label) &&
      Math.hypot(n.x - w.x, n.y - w.y) < r
    );
  }

  /* ── Events ── */
  bindEvents() {
    const c = this.canvas;
    c.addEventListener('mousedown', e => this.onMouseDown(e));
    c.addEventListener('mousemove', e => this.onMouseMove(e));
    c.addEventListener('mouseup',   e => this.onMouseUp(e));
    c.addEventListener('wheel',     e => this.onWheel(e), { passive: false });
    c.addEventListener('click',     e => this.onClick(e));
    window.addEventListener('resize', () => this.resize());
  }

  onMouseDown(e) {
    const node = this.getNodeAt(e.offsetX, e.offsetY);
    if (node) { this.dragging = node; }
    else       { this.isPanning = true; }
    this.lastMouse = { x: e.clientX, y: e.clientY };
  }

  onMouseMove(e) {
    const node = this.getNodeAt(e.offsetX, e.offsetY);
    this.hoveredNode = node;
    this.canvas.style.cursor = node ? 'pointer' : (this.isPanning ? 'grabbing' : 'grab');

    const dx = e.clientX - this.lastMouse.x, dy = e.clientY - this.lastMouse.y;
    if (this.dragging) {
      const w = this.screenToWorld(e.offsetX, e.offsetY);
      this.dragging.x = w.x; this.dragging.y = w.y;
      this.dragging.vx = 0;  this.dragging.vy = 0;
    } else if (this.isPanning) {
      this.panX += dx; this.panY += dy;
    }
    this.lastMouse = { x: e.clientX, y: e.clientY };
  }

  onMouseUp() {
    this.dragging = null; this.isPanning = false;
  }

  onWheel(e) {
    e.preventDefault();
    const factor = e.deltaY < 0 ? 1.1 : 0.91;
    this.zoom = Math.max(0.2, Math.min(4, this.zoom * factor));
  }

  onClick(e) {
    const node = this.getNodeAt(e.offsetX, e.offsetY);
    if (node && this.onNodeClick) { this.onNodeClick(node); }
    else if (!node && this.onCanvasClick) { this.onCanvasClick(); }
  }

  /* ── BFS shortest path ── */
  bfsPath(startId, endId) {
    const adj = {};
    this.nodes.forEach(n => { adj[n.id] = []; });
    this.edges.forEach(e => {
      if (adj[e.source]) adj[e.source].push(e.target);
      if (adj[e.target]) adj[e.target].push(e.source);
    });
    const visited = { [startId]: null };
    const queue   = [startId];
    while (queue.length) {
      const curr = queue.shift();
      if (curr === endId) break;
      (adj[curr] || []).forEach(nbr => {
        if (!(nbr in visited)) { visited[nbr] = curr; queue.push(nbr); }
      });
    }
    if (!(endId in visited)) return [];
    const path = []; let n = endId;
    while (n !== null) { path.unshift(n); n = visited[n]; }
    return path;
  }

  highlightPath(path) {
    this.pathNodes = path;
  }

  highlightQuery(ids) {
    this.queryNodes = ids;
  }

  focusNode(nodeId) {
    const n = this.nodes.find(x => x.id === nodeId);
    if (!n) return;
    const cx = this.canvas.width / 2, cy = this.canvas.height / 2;
    this.panX = (cx - n.x) * this.zoom;
    this.panY = (cy - n.y) * this.zoom;
  }

  addNode(node) {
    const cx = this.canvas.width / 2, cy = this.canvas.height / 2;
    node.x = cx + (Math.random() - .5) * 200;
    node.y = cy + (Math.random() - .5) * 200;
    node.vx = 0; node.vy = 0;
    this.nodes.push(node);
  }

  addEdge(edge) {
    const exists = this.edges.some(e => e.source === edge.source && e.target === edge.target && e.type === edge.type);
    if (!exists) this.edges.push(edge);
  }

  zoomIn()  { this.zoom = Math.min(4, this.zoom * 1.2); }
  zoomOut() { this.zoom = Math.max(0.2, this.zoom * 0.83); }
  clear()   { this.nodes = []; this.edges = []; this.selectedNode = null; this.pathNodes = []; this.queryNodes = []; }
}

/* ═══════════════════════════════════════════════════════════════
   HERO CANVAS (Landing background)
═══════════════════════════════════════════════════════════════ */
class HeroCanvas {
  constructor(id) {
    this.canvas = document.getElementById(id);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.nodes = [];
    this.resize();
    this.init();
    this.animate();
    window.addEventListener('resize', () => { this.resize(); this.init(); });
  }
  resize() {
    this.canvas.width  = this.canvas.offsetWidth;
    this.canvas.height = this.canvas.offsetHeight;
  }
  init() {
    this.nodes = Array.from({ length: 55 }, () => ({
      x: Math.random() * this.canvas.width,
      y: Math.random() * this.canvas.height,
      vx: (Math.random() - .5) * .5,
      vy: (Math.random() - .5) * .5,
      r: Math.random() * 2.5 + 1
    }));
  }
  animate() {
    const ctx = this.ctx, { width: W, height: H } = this.canvas;
    ctx.clearRect(0, 0, W, H);
    this.nodes.forEach(n => {
      n.x += n.vx; n.y += n.vy;
      if (n.x < 0 || n.x > W) n.vx *= -1;
      if (n.y < 0 || n.y > H) n.vy *= -1;
      ctx.beginPath(); ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
      ctx.fillStyle = Math.random() > .5 ? '#00d4a0' : '#4d9eff';
      ctx.fill();
    });
    for (let i = 0; i < this.nodes.length; i++) {
      for (let j = i + 1; j < this.nodes.length; j++) {
        const a = this.nodes[i], b = this.nodes[j];
        const d = Math.hypot(a.x - b.x, a.y - b.y);
        if (d < 130) {
          ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y);
          ctx.strokeStyle = `rgba(0,212,160,${(1 - d/130) * .15})`;
          ctx.lineWidth = .5; ctx.stroke();
        }
      }
    }
    requestAnimationFrame(() => this.animate());
  }
}

/* ═══════════════════════════════════════════════════════════════
   ENTITY EXTRACTION ENGINE
═══════════════════════════════════════════════════════════════ */
class EntityExtractor {
  extract(text) {
    const nodes = [], edges = [];
    const lower = text.toLowerCase();

    const PATTERNS = [
      { rx: /(\w[\w\s]+?)\s+founded\s+(\w[\w\s]+)/gi,         rel: 'FOUNDED',      srcLabel: 'Person',       tgtLabel: 'Organization' },
      { rx: /(\w[\w\s]+?)\s+co-?founded\s+(\w[\w\s]+)/gi,     rel: 'CO_FOUNDED',   srcLabel: 'Person',       tgtLabel: 'Organization' },
      { rx: /(\w[\w\s]+?)\s+acquired\s+(\w[\w\s]+)/gi,        rel: 'ACQUIRED',     srcLabel: 'Organization', tgtLabel: 'Organization' },
      { rx: /(\w[\w\s]+?)\s+(?:is\s+)?ceo\s+of\s+(\w[\w\s]+)/gi, rel: 'LEADS',    srcLabel: 'Person',       tgtLabel: 'Organization' },
      { rx: /(\w[\w\s]+?)\s+works?\s+(?:at|for)\s+(\w[\w\s]+)/gi, rel: 'WORKS_AT', srcLabel: 'Person',      tgtLabel: 'Organization' },
      { rx: /(\w[\w\s]+?)\s+(?:is\s+)?headquartered\s+in\s+(\w[\w\s]+)/gi, rel: 'HEADQUARTERED_IN', srcLabel: 'Organization', tgtLabel: 'Location' },
      { rx: /(\w[\w\s]+?)\s+(?:is\s+)?located\s+in\s+(\w[\w\s]+)/gi, rel: 'LOCATED_IN', srcLabel: 'Organization', tgtLabel: 'Location' },
      { rx: /(\w[\w\s]+?)\s+launched\s+(\w[\w\s]+)/gi,        rel: 'LAUNCHED',     srcLabel: 'Organization', tgtLabel: 'Product' },
      { rx: /(\w[\w\s]+?)\s+invented\s+(\w[\w\s]+)/gi,        rel: 'INVENTED',     srcLabel: 'Person',       tgtLabel: 'Concept' },
      { rx: /(\w[\w\s]+?)\s+discovered\s+(\w[\w\s]+)/gi,      rel: 'DISCOVERED',   srcLabel: 'Person',       tgtLabel: 'Concept' },
      { rx: /(\w[\w\s]+?)\s+invested\s+in\s+(\w[\w\s]+)/gi,   rel: 'INVESTED_IN',  srcLabel: 'Person',       tgtLabel: 'Organization' },
      { rx: /(\w[\w\s]+?)\s+partnered\s+with\s+(\w[\w\s]+)/gi,rel: 'PARTNER_OF',   srcLabel: 'Organization', tgtLabel: 'Organization' }
    ];

    const nodeMap = {};
    const addNode = (name, label) => {
      const clean = name.trim().replace(/\s+/g, ' ');
      if (clean.length < 2 || clean.length > 40) return null;
      if (!nodeMap[clean]) {
        const id = 'ex_' + Date.now() + '_' + Math.random().toString(36).slice(2, 6);
        nodeMap[clean] = { id, name: clean, label, desc: `Extracted entity` };
        nodes.push(nodeMap[clean]);
      }
      return nodeMap[clean];
    };

    PATTERNS.forEach(p => {
      let m;
      const rx = new RegExp(p.rx.source, p.rx.flags);
      while ((m = rx.exec(text)) !== null) {
        const src = addNode(m[1], p.srcLabel);
        const tgt = addNode(m[2], p.tgtLabel);
        if (src && tgt) {
          edges.push({ source: src.id, target: tgt.id, type: p.rel });
        }
      }
    });

    // Fallback: extract capitalised proper nouns if nothing matched
    if (nodes.length === 0) {
      const capWords = [...text.matchAll(/\b([A-Z][a-z]+(?: [A-Z][a-z]+)*)\b/g)]
        .map(m => m[1]).filter(w => w.length > 2);
      const unique = [...new Set(capWords)].slice(0, 10);
      unique.forEach((w, i) => {
        const label = i % 3 === 0 ? 'Person' : i % 3 === 1 ? 'Organization' : 'Concept';
        addNode(w, label);
      });
      // Connect sequentially
      const nodeArr = Object.values(nodeMap);
      for (let i = 1; i < nodeArr.length; i++) {
        edges.push({ source: nodeArr[i-1].id, target: nodeArr[i].id, type: 'RELATED_TO' });
      }
    }

    return { nodes, edges };
  }
}

/* ═══════════════════════════════════════════════════════════════
   CYPHER ENGINE (client-side interpreter)
═══════════════════════════════════════════════════════════════ */
class CypherEngine {
  constructor(getGraph) { this.getGraph = getGraph; }

  run(query) {
    const g = this.getGraph();
    const q = query.trim();
    const nodes = g.nodes.filter(n => !g.hiddenLabels.has(n.label));

    // MATCH (n) RETURN n
    if (/^MATCH\s*\(n\)\s*RETURN\s*n$/i.test(q)) {
      return { nodes: nodes, message: `${nodes.length} nodes returned` };
    }

    // MATCH (n:Label) RETURN n
    const labelMatch = q.match(/^MATCH\s*\(n:(\w+)\)\s*RETURN\s*n$/i);
    if (labelMatch) {
      const label = labelMatch[1];
      const res = nodes.filter(n => n.label.toLowerCase() === label.toLowerCase());
      return { nodes: res, message: `${res.length} nodes with label :${label}` };
    }

    // MATCH (n {name:"X"}) RETURN n
    const nameMatch = q.match(/^MATCH\s*\(n\s*\{name:\s*["'](.+?)["']\}\)\s*RETURN\s*n$/i);
    if (nameMatch) {
      const name = nameMatch[1];
      const res = nodes.filter(n => n.name.toLowerCase().includes(name.toLowerCase()));
      return { nodes: res, message: `${res.length} nodes matching name "${name}"` };
    }

    // MATCH (a)-[r]->(b) RETURN a,r,b
    if (/^MATCH\s*\(a\)\s*-\[r\]->\s*\(b\)\s*RETURN\s*a,r,b$/i.test(q)) {
      return { nodes: nodes, message: `${nodes.length} nodes, ${g.edges.length} relationships` };
    }

    // MATCH (a)-[r:TYPE]->(b) RETURN a,b
    const relTypeMatch = q.match(/^MATCH\s*\(a\)\s*-\[r:(\w+)\]->\s*\(b\)\s*RETURN\s*a,b$/i);
    if (relTypeMatch) {
      const type = relTypeMatch[1].toUpperCase();
      const relEdges = g.edges.filter(e => e.type === type);
      const ids = new Set();
      relEdges.forEach(e => { ids.add(e.source); ids.add(e.target); });
      const res = nodes.filter(n => ids.has(n.id));
      return { nodes: res, message: `${res.length} nodes in ${relEdges.length} [${type}] relationships` };
    }

    // MATCH (a:Label)-[r]->(b) RETURN a,b
    const labelRelMatch = q.match(/^MATCH\s*\(a:(\w+)\)\s*-\[r\]->\s*\(b\)\s*RETURN\s*a,b$/i);
    if (labelRelMatch) {
      const label = labelRelMatch[1];
      const srcNodes = nodes.filter(n => n.label.toLowerCase() === label.toLowerCase());
      const tgtIds = new Set();
      srcNodes.forEach(src => {
        g.edges.filter(e => e.source === src.id).forEach(e => tgtIds.add(e.target));
      });
      const res = [...srcNodes, ...nodes.filter(n => tgtIds.has(n.id))];
      const unique = res.filter((n, i, a) => a.findIndex(x => x.id === n.id) === i);
      return { nodes: unique, message: `${unique.length} nodes in :${label} relationships` };
    }

    return { nodes: [], message: `⚠ Unrecognised pattern. Try MATCH (n) RETURN n` };
  }
}

/* ═══════════════════════════════════════════════════════════════
   MAIN APP CONTROLLER
═══════════════════════════════════════════════════════════════ */
class App {
  constructor() {
    this.currentDataset  = 'movies';
    this.currentMode     = 'explore';
    this.pathStep        = 0;   // 0=idle 1=pick-src 2=pick-tgt
    this.pathSrc         = null;
    this.physics         = null;
    this.extractor       = new EntityExtractor();

    this.init();
  }

  init() {
    // Landing
    document.getElementById('btn-launch-workspace')?.addEventListener('click', () => this.showWorkspace());
    document.getElementById('btn-enter-workspace') ?.addEventListener('click', () => this.showWorkspace());
    document.getElementById('btn-open-workspace-2')?.addEventListener('click', () => this.showWorkspace());
    document.querySelectorAll('.dataset-card').forEach(c =>
      c.addEventListener('click', () => {
        this.showWorkspace();
        setTimeout(() => this.switchDataset(c.dataset.dataset), 300);
      })
    );

    // Workspace back
    document.getElementById('btn-back-to-landing')?.addEventListener('click', () => this.showLanding());

    // Mode tabs
    document.querySelectorAll('.ws-mode-tab').forEach(b =>
      b.addEventListener('click', () => this.setMode(b.dataset.mode))
    );

    // Dataset buttons
    document.querySelectorAll('.ds-btn').forEach(b =>
      b.addEventListener('click', () => this.switchDataset(b.dataset.dataset))
    );

    // Canvas toolbar
    document.getElementById('btn-reset-view') ?.addEventListener('click', () => { this.physics?.resetView(); });
    document.getElementById('btn-zoom-in')    ?.addEventListener('click', () => { this.physics?.zoomIn(); this.updateZoomLabel(); });
    document.getElementById('btn-zoom-out')   ?.addEventListener('click', () => { this.physics?.zoomOut(); this.updateZoomLabel(); });
    document.getElementById('btn-add-node')   ?.addEventListener('click', () => this.openAddNodeModal());
    document.getElementById('btn-clear-canvas')?.addEventListener('click', () => this.clearCanvas());

    // Search
    document.getElementById('ws-search')?.addEventListener('input', e => this.handleSearch(e.target.value));

    // Path cancel
    document.getElementById('btn-cancel-path')?.addEventListener('click', () => this.cancelPath());

    // Right panel tabs
    document.querySelectorAll('.rp-tab').forEach(b =>
      b.addEventListener('click', () => this.setRpTab(b.dataset.rptab))
    );

    // Quick queries
    document.querySelectorAll('.quick-query').forEach(q =>
      q.addEventListener('click', () => {
        document.getElementById('cypher-input').value = q.dataset.query;
        this.setRpTab('cypher');
        this.runCypher(q.dataset.query);
      })
    );

    // Cypher run / clear
    document.getElementById('btn-run-cypher') ?.addEventListener('click', () => this.runCypher());
    document.getElementById('btn-clear-cypher')?.addEventListener('click', () => {
      document.getElementById('cypher-input').value = '';
      document.getElementById('cypher-results').innerHTML = '<div class="cypher-results-empty">Results will appear here. Try <code>MATCH (n) RETURN n</code></div>';
      this.physics?.highlightQuery([]);
    });
    document.getElementById('cypher-input')?.addEventListener('keydown', e => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') this.runCypher();
    });

    // Extract
    document.getElementById('btn-extract')?.addEventListener('click', () => this.runExtraction());

    // Solutions
    document.querySelectorAll('.solution-item').forEach(s =>
      s.addEventListener('click', () => this.openSolution(s.dataset.sol))
    );
    document.getElementById('btn-close-modal')?.addEventListener('click', () => this.closeSolution());
    document.getElementById('sol-modal-backdrop')?.addEventListener('click', () => this.closeSolution());

    // Add node modal
    document.getElementById('btn-close-add-node')  ?.addEventListener('click', () => this.closeAddNodeModal());
    document.getElementById('btn-cancel-add-node') ?.addEventListener('click', () => this.closeAddNodeModal());
    document.getElementById('btn-confirm-add-node')?.addEventListener('click', () => this.confirmAddNode());
    document.getElementById('add-node-backdrop')   ?.addEventListener('click', () => this.closeAddNodeModal());

    // Query result bar close
    document.getElementById('btn-close-result')?.addEventListener('click', () => {
      document.getElementById('query-result-bar').classList.add('hidden');
      this.physics?.highlightQuery([]);
    });
  }

  /* ── Landing / Workspace toggle ── */
  showWorkspace() {
    document.getElementById('landing-page').classList.add('hidden');
    const ws = document.getElementById('workspace-app');
    ws.classList.remove('hidden');
    if (!this.physics) this.initPhysics();
  }

  showLanding() {
    document.getElementById('workspace-app').classList.add('hidden');
    document.getElementById('landing-page').classList.remove('hidden');
  }

  /* ── Init physics canvas ── */
  initPhysics() {
    const canvas = document.getElementById('graph-canvas');
    this.physics = new GraphPhysics(canvas);
    this.cypher  = new CypherEngine(() => this.physics);

    this.physics.onNodeClick = (node) => this.handleNodeClick(node);
    this.physics.onCanvasClick = () => {
      if (this.currentMode !== 'path') {
        this.physics.selectedNode = null;
        this.showInspectorEmpty();
      }
    };

    // Update zoom label on wheel
    canvas.addEventListener('wheel', () => setTimeout(() => this.updateZoomLabel(), 50), { passive: true });

    this.switchDataset('movies');
    this.initHeroCanvas();

    // Live zoom label update
    setInterval(() => this.updateZoomLabel(), 500);
  }

  initHeroCanvas() { new HeroCanvas('hero-canvas'); }

  /* ── Dataset ── */
  switchDataset(key) {
    if (!DATASETS[key]) return;
    this.currentDataset = key;

    // Update sidebar buttons
    document.querySelectorAll('.ds-btn').forEach(b =>
      b.classList.toggle('active', b.dataset.dataset === key)
    );

    this.physics.loadDataset(DATASETS[key]);
    this.physics.hiddenLabels.clear();
    this.cancelPath();
    this.physics.selectedNode = null;
    this.showInspectorEmpty();
    this.physics.highlightQuery([]);

    this.buildLabelFilters();
    this.updateStats();
    this.buildTopConnected();
    this.updateZoomLabel();

    document.getElementById('query-result-bar').classList.add('hidden');
  }

  /* ── Label filters ── */
  buildLabelFilters() {
    const labels = [...new Set(this.physics.nodes.map(n => n.label))];
    const container = document.getElementById('label-filters');
    container.innerHTML = '';
    labels.forEach(label => {
      const count = this.physics.nodes.filter(n => n.label === label).length;
      const color = labelColor(label);
      const item = document.createElement('label');
      item.className = 'label-filter-item';
      item.innerHTML = `
        <input type="checkbox" checked data-label="${label}" />
        <span class="label-dot" style="background:${color}"></span>
        <span class="label-filter-name">${label}</span>
        <span class="label-filter-count">${count}</span>
      `;
      item.querySelector('input').addEventListener('change', e => {
        if (e.target.checked) this.physics.hiddenLabels.delete(label);
        else                  this.physics.hiddenLabels.add(label);
        this.updateStats();
      });
      container.appendChild(item);
    });
  }

  /* ── Stats ── */
  updateStats() {
    const visible = this.physics.nodes.filter(n => !this.physics.hiddenLabels.has(n.label));
    const labels  = [...new Set(visible.map(n => n.label))];
    document.getElementById('stat-nodes').textContent  = visible.length;
    document.getElementById('stat-edges').textContent  = this.physics.edges.length;
    document.getElementById('stat-labels').textContent = labels.length;
  }

  /* ── Top connected ── */
  buildTopConnected() {
    const degMap = {};
    this.physics.nodes.forEach(n => { degMap[n.id] = 0; });
    this.physics.edges.forEach(e => {
      if (degMap[e.source] !== undefined) degMap[e.source]++;
      if (degMap[e.target] !== undefined) degMap[e.target]++;
    });
    const sorted = Object.entries(degMap).sort((a, b) => b[1] - a[1]).slice(0, 5);
    const container = document.getElementById('top-connected');
    container.innerHTML = '';
    sorted.forEach(([id, deg]) => {
      const node = this.physics.nodes.find(n => n.id === id);
      if (!node) return;
      const item = document.createElement('div');
      item.className = 'top-conn-item';
      item.innerHTML = `<span>${node.name}</span><span class="top-conn-count">${deg}</span>`;
      item.addEventListener('click', () => {
        this.physics.selectedNode = node;
        this.physics.focusNode(node.id);
        this.showInspector(node);
      });
      container.appendChild(item);
    });
  }

  /* ── Mode ── */
  setMode(mode) {
    this.currentMode = mode;
    document.querySelectorAll('.ws-mode-tab').forEach(b =>
      b.classList.toggle('active', b.dataset.mode === mode)
    );
    this.cancelPath();

    if (mode === 'path') {
      this.pathStep = 1;
      this.showPathBanner('Click a <strong>source</strong> node on the canvas');
    } else if (mode === 'query') {
      this.setRpTab('cypher');
    } else if (mode === 'solutions') {
      this.setRpTab('solutions');
    } else {
      document.getElementById('path-mode-banner').classList.add('hidden');
    }
  }

  cancelPath() {
    this.pathStep = 0; this.pathSrc = null;
    this.physics?.highlightPath([]);
    document.getElementById('path-mode-banner').classList.add('hidden');
  }

  showPathBanner(html) {
    const banner = document.getElementById('path-mode-banner');
    banner.classList.remove('hidden');
    document.getElementById('path-banner-text').innerHTML = html;
  }

  /* ── Node click ── */
  handleNodeClick(node) {
    if (this.currentMode === 'path') {
      if (this.pathStep === 1) {
        this.pathSrc  = node;
        this.pathStep = 2;
        this.showPathBanner(`Source: <strong>${node.name}</strong> — now click a <strong>target</strong> node`);
      } else if (this.pathStep === 2) {
        const path = this.physics.bfsPath(this.pathSrc.id, node.id);
        if (path.length > 0) {
          this.physics.highlightPath(path);
          const names = path.map(id => this.physics.nodes.find(n => n.id === id)?.name).join(' → ');
          this.showPathBanner(`Path (${path.length} nodes): ${names}`);
        } else {
          this.showPathBanner(`No path found between <strong>${this.pathSrc.name}</strong> and <strong>${node.name}</strong>`);
        }
        this.pathStep = 1;
        this.pathSrc  = null;
      }
      return;
    }

    this.physics.selectedNode = node;
    this.showInspector(node);
    this.setRpTab('inspector');
  }

  /* ── Inspector ── */
  showInspectorEmpty() {
    document.getElementById('inspector-empty')  .classList.remove('hidden');
    document.getElementById('inspector-content').classList.add('hidden');
  }

  showInspector(node) {
    document.getElementById('inspector-empty')  .classList.add('hidden');
    document.getElementById('inspector-content').classList.remove('hidden');

    const color = labelColor(node.label);
    document.getElementById('inspector-dot')  .style.background = color;
    document.getElementById('inspector-name') .textContent = node.name;
    document.getElementById('inspector-label').textContent = node.label.toUpperCase();

    // Props
    const propsEl = document.getElementById('inspector-props');
    propsEl.innerHTML = '';
    const props = { id: node.id, label: node.label, name: node.name };
    if (node.desc) props.description = node.desc;
    Object.entries(props).forEach(([k, v]) => {
      const row = document.createElement('div');
      row.className = 'inspector-prop';
      row.innerHTML = `<span class="prop-key">${k}</span><span class="prop-val">${v}</span>`;
      propsEl.appendChild(row);
    });

    // Relationships
    const relsEl = document.getElementById('inspector-rels');
    relsEl.innerHTML = '';
    const outgoing = this.physics.edges.filter(e => e.source === node.id);
    const incoming = this.physics.edges.filter(e => e.target === node.id);
    [...outgoing.map(e => ({ dir: '→', type: e.type, other: e.target })),
     ...incoming.map(e => ({ dir: '←', type: e.type, other: e.source }))]
    .forEach(r => {
      const other = this.physics.nodes.find(n => n.id === r.other);
      if (!other) return;
      const row = document.createElement('div');
      row.className = 'inspector-rel';
      row.innerHTML = `<span class="rel-dir">${r.dir}</span><span class="rel-type">[${r.type}]</span><span class="rel-target">${other.name}</span>`;
      relsEl.appendChild(row);
    });
    if (relsEl.children.length === 0) {
      relsEl.innerHTML = '<div style="font-size:11px;color:var(--text3)">No relationships</div>';
    }
  }

  /* ── Right panel tab ── */
  setRpTab(tab) {
    document.querySelectorAll('.rp-tab').forEach(b => b.classList.toggle('active', b.dataset.rptab === tab));
    document.querySelectorAll('.rp-content').forEach(c => c.classList.toggle('active', c.id === `rp-${tab}`));
  }

  /* ── Cypher ── */
  runCypher(queryOverride) {
    const q = queryOverride || document.getElementById('cypher-input').value.trim();
    if (!q) return;
    const result = this.cypher.run(q);
    const resultsEl = document.getElementById('cypher-results');
    resultsEl.innerHTML = '';

    if (result.nodes.length === 0) {
      resultsEl.innerHTML = `<div class="cypher-results-empty">${result.message}</div>`;
      return;
    }

    result.nodes.forEach(n => {
      const color = labelColor(n.label);
      const row = document.createElement('div');
      row.className = 'cypher-result-node';
      row.innerHTML = `
        <span class="cypher-result-dot" style="background:${color}"></span>
        <span class="cypher-result-name">${n.name}</span>
        <span class="cypher-result-label">${n.label}</span>
      `;
      row.addEventListener('click', () => {
        this.physics.selectedNode = n;
        this.physics.focusNode(n.id);
        this.showInspector(n);
        this.setRpTab('inspector');
      });
      resultsEl.appendChild(row);
    });

    // Highlight on canvas
    this.physics.highlightQuery(result.nodes.map(n => n.id));
    const bar = document.getElementById('query-result-bar');
    document.getElementById('query-result-text').textContent = result.message;
    bar.classList.remove('hidden');
  }

  /* ── Entity extraction ── */
  runExtraction() {
    const text = document.getElementById('extract-input').value.trim();
    if (!text) return;

    const log = document.getElementById('extract-log');
    log.classList.remove('hidden');
    log.innerHTML = '';

    const addLog = (msg, type = 'info') => {
      const line = document.createElement('div');
      line.className = `extract-log-line ${type}`;
      line.textContent = msg;
      log.appendChild(line);
      log.scrollTop = log.scrollHeight;
    };

    addLog('› Analysing text…', 'info');
    const { nodes, edges } = this.extractor.extract(text);
    addLog(`› Found ${nodes.length} entities, ${edges.length} relationships`, 'info');

    let delay = 200;
    nodes.forEach(node => {
      setTimeout(() => {
        this.physics.addNode(node);
        addLog(`+ Node: ${node.name} (${node.label})`, 'node-added');
        this.updateStats();
        this.buildTopConnected();
      }, delay);
      delay += 150;
    });

    edges.forEach(edge => {
      setTimeout(() => {
        this.physics.addEdge(edge);
        const src = nodes.find(n => n.id === edge.source);
        const tgt = nodes.find(n => n.id === edge.target);
        if (src && tgt) {
          addLog(`→ Edge: (${src.name})-[${edge.type}]->(${tgt.name})`, 'edge-added');
        }
        this.updateStats();
      }, delay);
      delay += 150;
    });

    setTimeout(() => {
      addLog(`✓ Done — ${nodes.length} nodes added to graph`, 'node-added');
      this.buildLabelFilters();
    }, delay + 100);
  }

  /* ── Search ── */
  handleSearch(query) {
    if (!query.trim()) { this.physics.highlightQuery([]); return; }
    const q = query.toLowerCase();
    const matches = this.physics.nodes.filter(n =>
      n.name.toLowerCase().includes(q) || n.label.toLowerCase().includes(q)
    );
    this.physics.highlightQuery(matches.map(n => n.id));
    if (matches.length === 1) this.physics.focusNode(matches[0].id);
  }

  /* ── Add node ── */
  openAddNodeModal() {
    document.getElementById('add-node-modal').classList.remove('hidden');
    document.getElementById('new-node-name').focus();
  }
  closeAddNodeModal() {
    document.getElementById('add-node-modal').classList.add('hidden');
  }
  confirmAddNode() {
    const name  = document.getElementById('new-node-name').value.trim();
    const label = document.getElementById('new-node-label').value;
    const desc  = document.getElementById('new-node-desc').value.trim();
    if (!name) return;
    const id = 'manual_' + Date.now();
    this.physics.addNode({ id, name, label, desc: desc || label });
    this.updateStats(); this.buildTopConnected(); this.buildLabelFilters();
    this.closeAddNodeModal();
    document.getElementById('new-node-name').value = '';
    document.getElementById('new-node-desc').value = '';
  }

  clearCanvas() {
    this.physics.clear();
    this.updateStats(); this.buildTopConnected(); this.buildLabelFilters();
    this.showInspectorEmpty();
    document.getElementById('query-result-bar').classList.add('hidden');
  }

  /* ── Solutions modal ── */
  openSolution(key) {
    const sol = SOLUTIONS[key]; if (!sol) return;
    document.getElementById('sol-modal-title').textContent = sol.title;
    document.getElementById('sol-modal-body').innerHTML   = sol.body;
    document.getElementById('solution-modal').classList.remove('hidden');
  }
  closeSolution() {
    document.getElementById('solution-modal').classList.add('hidden');
  }

  /* ── Zoom label ── */
  updateZoomLabel() {
    if (!this.physics) return;
    document.getElementById('zoom-label').textContent = `${Math.round(this.physics.zoom * 100)}%`;
  }
}

/* ── Boot ── */
window.addEventListener('DOMContentLoaded', () => {
  new HeroCanvas('hero-canvas');
  window._app = new App();
});
