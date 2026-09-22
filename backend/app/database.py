"""
MongoDB Atlas Connection — Motor (async driver)

No local install needed.
Free forever on MongoDB Atlas M0 tier (512MB).

Setup:
1. mongodb.com/atlas → Create free account
2. Create FREE cluster (M0 - Shared)
3. Database Access → Add user → username + password
4. Network Access → Add IP → 0.0.0.0/0 (allow all)
5. Clusters → Connect → Drivers → Copy connection string
6. Paste in .env as MONGODB_URL
"""

from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

# Global client — created once on startup
_client: AsyncIOMotorClient = None
_db = None


def get_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.mongodb_url)
    return _client


def get_db():
    """Returns the ipsakti database handle"""
    return get_client()["ipsakti"]


# ── Collection helpers ───────────────────────────────────────

def chat_sessions():
    return get_db()["chat_sessions"]

def chat_messages():
    return get_db()["chat_messages"]

def audit_logs():
    return get_db()["audit_logs"]

def biopiracy_alerts():
    return get_db()["biopiracy_alerts"]


# ── Startup / Shutdown ───────────────────────────────────────

async def connect_db():
    """Called on FastAPI startup — test connection"""
    client = get_client()
    await client.admin.command("ping")
    print("MongoDB Atlas connected successfully.")


async def close_db():
    """Called on FastAPI shutdown"""
    global _client
    if _client:
        _client.close()
        _client = None
