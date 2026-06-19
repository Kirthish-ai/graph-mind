"""
database.py — MongoDB connection and collection accessors.
Database: graphmind
Collections: datasets, nodes, edges
"""

from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from pymongo.collection import Collection
from pymongo.database import Database

MONGO_URI = "mongodb://localhost:27017"
DB_NAME   = "graphmind"

# ── Singleton connection ───────────────────────────────────────────────────────
_client: MongoClient | None = None
_db:     Database | None     = None


def get_db() -> Database:
    global _client, _db
    if _db is None:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        _db = _client[DB_NAME]
        _ensure_indexes(_db)
        print(f"[MongoDB] Connected → {MONGO_URI}/{DB_NAME}")
    return _db


def _ensure_indexes(db: Database):
    """Create indexes for fast lookups."""
    # datasets
    db.datasets.create_index([("key", ASCENDING)], unique=True)

    # nodes
    db.nodes.create_index([("dataset", ASCENDING), ("id",    ASCENDING)], unique=True)
    db.nodes.create_index([("dataset", ASCENDING), ("label", ASCENDING)])
    db.nodes.create_index([("dataset", ASCENDING), ("name",  TEXT)])

    # edges
    db.edges.create_index([("dataset", ASCENDING), ("id",     ASCENDING)], unique=True)
    db.edges.create_index([("dataset", ASCENDING), ("source", ASCENDING)])
    db.edges.create_index([("dataset", ASCENDING), ("target", ASCENDING)])
    db.edges.create_index([("dataset", ASCENDING), ("type",   ASCENDING)])

    print("[MongoDB] Indexes ensured.")


def collections() -> tuple[Collection, Collection, Collection]:
    """Return (datasets_col, nodes_col, edges_col)."""
    db = get_db()
    return db.datasets, db.nodes, db.edges
