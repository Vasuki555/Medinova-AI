"""
MongoDB Database Connection
Handles MongoDB Atlas connection using Motor (async driver)
Falls back to mongomock in-memory database when Atlas is unreachable.
"""

import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import settings

logger = logging.getLogger(__name__)

# Track whether we are using a mock database
_using_mock = False


def _create_mock_db():
    """
    Create an async-compatible in-memory MongoDB mock.
    Used as a fallback when Atlas is not reachable.
    """
    try:
        import mongomock
        import mongomock.mongo_client

        mock_client = mongomock.MongoClient()
        mock_db = mock_client[settings.MONGODB_DB_NAME]
        logger.warning(
            "[MOCK DB] Using in-memory mongomock database. "
            "Data will NOT persist between restarts. "
            "Fix MongoDB Atlas IP whitelist for production use."
        )
        return mock_client, mock_db
    except ImportError:
        logger.error("mongomock not installed. Run: pip install mongomock")
        raise


class MockAsyncDatabase:
    """
    Thin async wrapper around a synchronous mongomock database,
    providing the same interface as AsyncIOMotorDatabase.
    """
    def __init__(self, mock_db):
        self._db = mock_db

    def __getitem__(self, name):
        return MockAsyncCollection(self._db[name])

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        return MockAsyncCollection(getattr(self._db, name))


class MockAsyncCollection:
    """Async wrapper around a synchronous mongomock collection."""
    def __init__(self, col):
        self._col = col

    async def find_one(self, *a, **kw):
        return self._col.find_one(*a, **kw)

    def find(self, *a, **kw):
        return MockAsyncCursor(self._col.find(*a, **kw))

    async def insert_one(self, *a, **kw):
        return self._col.insert_one(*a, **kw)

    async def insert_many(self, *a, **kw):
        return self._col.insert_many(*a, **kw)

    async def update_one(self, *a, **kw):
        return self._col.update_one(*a, **kw)

    async def update_many(self, *a, **kw):
        return self._col.update_many(*a, **kw)

    async def delete_one(self, *a, **kw):
        return self._col.delete_one(*a, **kw)

    async def delete_many(self, *a, **kw):
        return self._col.delete_many(*a, **kw)

    async def count_documents(self, *a, **kw):
        return self._col.count_documents(*a, **kw)

    async def create_index(self, *a, **kw):
        return self._col.create_index(*a, **kw)

    async def aggregate(self, pipeline, **kw):
        return MockAsyncCursor(self._col.aggregate(pipeline))


class MockAsyncCursor:
    """Async wrapper for mongomock cursor."""
    def __init__(self, cursor):
        self._cursor = cursor
        self._items = None

    def sort(self, *a, **kw):
        self._cursor = self._cursor.sort(*a, **kw)
        return self

    def skip(self, n):
        self._cursor = self._cursor.skip(n)
        return self

    def limit(self, n):
        self._cursor = self._cursor.limit(n)
        return self

    async def to_list(self, length=None):
        items = list(self._cursor)
        if length is not None:
            return items[:length]
        return items

    def __aiter__(self):
        self._items = iter(list(self._cursor))
        return self

    async def __anext__(self):
        try:
            return next(self._items)
        except StopIteration:
            raise StopAsyncIteration


class Database:
    """MongoDB database connection manager"""

    client = None
    database = None

    @classmethod
    async def connect_to_database(cls):
        """
        Connect to MongoDB Atlas.
        If Atlas is unreachable, fall back to in-memory mongomock.
        """
        global _using_mock

        # --- Attempt Atlas connection ---
        try:
            logger.info("Connecting to MongoDB Atlas...")
            
            # Simple connection for Python 3.14 compatibility
            # The connection string in .env already has tlsAllowInvalidCertificates=true
            atlas_client = AsyncIOMotorClient(
                settings.MONGODB_URL,
                minPoolSize=1,
                maxPoolSize=settings.MONGODB_MAX_POOL_SIZE,
                serverSelectionTimeoutMS=10000,
                connectTimeoutMS=10000,
                socketTimeoutMS=10000,
                retryWrites=True,
                w="majority",
            )

            # Ping to confirm reachability
            await atlas_client.admin.command("ping")

            cls.client = atlas_client
            cls.database = atlas_client[settings.MONGODB_DB_NAME]
            _using_mock = False
            logger.info(f"[OK] Connected to MongoDB Atlas -- database: {settings.MONGODB_DB_NAME}")
            return

        except Exception as atlas_err:
            logger.warning(
                f"MongoDB Atlas unreachable: {type(atlas_err).__name__}: {str(atlas_err)}. "
                "Falling back to in-memory mongomock."
            )

        # --- Fallback: in-memory mock (development only) ---
        if settings.is_production:
            logger.error("MongoDB Atlas connection failed in PRODUCTION environment")
            logger.error("Production cannot run without persistent database")
            raise RuntimeError(
                "MongoDB Atlas connection required for production. "
                "Check connection string, network access, and TLS certificates."
            )
        
        # Development fallback
        try:
            _, mock_db = _create_mock_db()
            cls.database = MockAsyncDatabase(mock_db)
            cls.client = None
            _using_mock = True
        except Exception as mock_err:
            logger.error(f"Mongomock fallback also failed: {mock_err}")
            raise

    @classmethod
    async def close_database_connection(cls):
        """Close MongoDB connection (if real client exists)."""
        try:
            if cls.client:
                logger.info("Closing MongoDB connection...")
                cls.client.close()
                logger.info("MongoDB connection closed.")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {e}")

    @classmethod
    def get_database(cls):
        """Get database instance."""
        if cls.database is None:
            raise Exception("Database not connected. Call connect_to_database() first.")
        return cls.database

    @classmethod
    def is_using_mock(cls) -> bool:
        """Returns True when running on in-memory mock DB."""
        return _using_mock

    @classmethod
    async def check_connection(cls) -> bool:
        """Check if database connection is healthy."""
        try:
            if _using_mock:
                return True   # mock is always 'up'
            if cls.client:
                await cls.client.admin.command("ping")
                return True
            return False
        except Exception:
            return False


# Dependency injection for routes
async def get_database():
    """
    FastAPI dependency to get database instance.
    Usage: db = Depends(get_database)
    """
    return Database.get_database()
