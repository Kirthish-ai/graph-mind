# GraphMind — Knowledge Graph Studio

GraphMind is a Neo4j-inspired knowledge graph engine and interactive studio with cinematic force-directed physics. It allows you to explore connected datasets, run Cypher-lite queries, find shortest paths, and perform NLP-based semantic entity extraction from raw text.

The project is structured to offer two ways to run the application:
1. **A Zero-Install Static Web App**: Runs completely client-side inside any modern web browser.
2. **A Distributed Database-Backed Application**: Backed by a Python FastAPI server, a Streamlit dashboard, and MongoDB.

---

##  Project Directory Structure

```text
Graphmind/
├── index.html          # Static Web App UI (HTML5 Entry Point)
├── style.css           # Styling for the Static Web App
├── app.js              # Physics engine, client-side Cypher, and UI logic
├── backend/            # Python FastAPI Backend
│   ├── main.py         # FastAPI API endpoints and server setup
│   ├── database.py     # MongoDB connection management & indexing
│   ├── graph_store.py  # Sharding, CRUD, shortest path, and Cypher logic
│   ├── requirements.txt# Backend Python dependencies
│   └── start.sh        # Setup script (creates virtual environment, runs server)
├── frontend/           # Python Streamlit Frontend
│   ├── app.py          # Dashboard UI & visualization layouts
│   └── start.sh        # Startup script for Streamlit
└── .vscode/            # Workspace configuration profiles
```

---

##  Prerequisites & Installation Requirements

Depending on how you wish to run GraphMind, ensure you meet the following requirements:

### For the Static Web App (Option 1)
* **Web Browser**: Any modern browser (Chrome, Safari, Firefox, Edge, etc.)
* **No installations required** (completely self-contained).

### For the Database-Backed Stack (Option 2)
* **Python**: Python 3.10 or higher.
* **MongoDB**: A running instance of MongoDB on your system (defaults to connection at `mongodb://localhost:27017`).
* **Shell**: A bash/zsh terminal (macOS/Linux) to run the startup script automations.

---

##  How to Run GraphMind

### Option 1: Standalone Static Web App (Zero-Install, Client-Side)
This is the fastest way to explore the application using pre-seeded datasets and in-browser mock engines for Cypher and Shortest Path.
1. Locate `index.html` in the root folder.
2. Double-click `index.html` (or drag and drop it into a browser tab).
3. The interface will boot immediately!

---

### Option 2: Full Python + FastAPI + MongoDB + Streamlit Stack
This configuration runs a FastAPI server connected to a local MongoDB database and serves the dashboard via Streamlit.

#### Step 1: Start MongoDB
Make sure your MongoDB server is up and running on your local machine.
* By default, it will look for: `mongodb://localhost:27017/graphmind`

#### Step 2: Start the Backend Server
Navigate to the `backend/` directory and execute the startup script. The script will automatically create a virtual environment (`venv`), install dependencies, and run the FastAPI server.

```bash
cd backend
chmod +x start.sh  # Ensure the script is executable
./start.sh
```

* **API Server URL**: `http://localhost:8000`
* **Interactive API Documentation**: `http://localhost:8000/docs` (Swagger UI)

#### Step 3: Start the Streamlit Frontend
Open a new terminal window, navigate to the `frontend/` directory, and run the startup script:

```bash
cd frontend
chmod +x start.sh  # Ensure the script is executable
./start.sh
```

* **Frontend Dashboard URL**: `http://localhost:8501`

---

##  Key Features to Explore

* **Force-Directed Physics Canvas**: Drag nodes around, watch the graph physics update in real-time, and zoom using your trackpad or scroll wheel.
* **Cypher-Lite queries**: Try running patterns like:
  ```cypher
  MATCH (n) RETURN n
  MATCH (n:Person) RETURN n
  MATCH (a)-[r]->(b) RETURN a,r,b
  ```
* **Shortest Path Finder**: Highlight the BFS path corridor between any two entities on the canvas.
* **Semantic Entity Extraction**: Go to the **EXTRACT** tab, paste a paragraph of raw text (e.g., *"Elon Musk founded Tesla and SpaceX. Tesla is headquartered in Austin."*), and see nodes and relationships generated and mapped on-screen instantly.
# graph-mind
