# db.py
import os
import logging
from typing import Optional, Dict, List, Any
from datetime import datetime
import uuid

from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential
from pymongo import MongoClient, ASCENDING, IndexModel
from pymongo.errors import ConnectionFailure, OperationFailure, ServerSelectionTimeoutError
from pymongo.server_api import ServerApi

load_dotenv()

logger = logging.getLogger(__name__)

class MongoDB:
    """
    A singleton MongoDB client wrapper.
    Provides a single instance of the MongoClient across the application.
    """
    _instance: Optional['MongoDB'] = None
    _client: Optional[MongoClient] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """
        Initialize the MongoDB client and database references.
        Uses environment variables to configure the connection.
        """
        if getattr(self, '_initialized', False):
            return  # Already initialized

        # Determine environment: dev, staging, or production
        env = os.getenv("ENV", "development").lower()  # e.g. "development" or "production"
        # Read MongoDB URI from environment
        uri = os.getenv("MONGODB_URI")
        if not uri:
            raise ValueError("MONGODB_URI environment variable is not set")

        # ---------------------
        # 1) Configure Pool & Timeout settings
        # You might want smaller pool sizes/timeouts locally for a lighter footprint
        if env == "development":
            max_pool_size = int(os.getenv("MONGO_MAX_POOL_SIZE", 5))
            min_pool_size = int(os.getenv("MONGO_MIN_POOL_SIZE", 0))
            connect_timeout_ms = int(os.getenv("MONGO_CONNECT_TIMEOUT_MS", 5000))
            socket_timeout_ms = int(os.getenv("MONGO_SOCKET_TIMEOUT_MS", 10000))
            server_selection_timeout_ms = int(os.getenv("MONGO_SERVER_SELECTION_TIMEOUT_MS", 5000))
            # In dev, you might also want "connect=False" so that it's lazily connected.
            # This helps avoid overhead if you never actually run a DB query.
            connect_now = False
        else:
            max_pool_size = int(os.getenv("MONGO_MAX_POOL_SIZE", 50))
            min_pool_size = int(os.getenv("MONGO_MIN_POOL_SIZE", 10))
            connect_timeout_ms = int(os.getenv("MONGO_CONNECT_TIMEOUT_MS", 10000))
            socket_timeout_ms = int(os.getenv("MONGO_SOCKET_TIMEOUT_MS", 45000))
            server_selection_timeout_ms = int(os.getenv("MONGO_SERVER_SELECTION_TIMEOUT_MS", 10000))
            connect_now = True

        # 2) Create MongoDB client with recommended production settings,
        #    or scaled-down dev settings
        self._client = MongoClient(
            uri,
            server_api=ServerApi('1'),
            maxPoolSize=max_pool_size,
            minPoolSize=min_pool_size,
            maxIdleTimeMS=int(os.getenv("MONGO_MAX_IDLE_TIME_MS", 30000)),
            connectTimeoutMS=connect_timeout_ms,
            socketTimeoutMS=socket_timeout_ms,
            serverSelectionTimeoutMS=server_selection_timeout_ms,
            retryWrites=True,
            w='majority',  # Adjust write concern as needed
            connect=connect_now,  # dev = False, prod = True
        )

        # Attach your main database
        self.db = self._client.nozomio

        # Collections
        self.projects = self.db.projects
        self.users = self.db.users
        self.chats = self.db.chats
        self.slack_installations = self.db.slack_installations
        self.api_keys = self.db.api_keys
        self.community_repos = self.db.community_repos
        self.nuanced_graphs = self.db.nuanced_graphs

        # Optionally skip index creation entirely in development
        # (or only ensure them once).
        # Adjust by using an ENV variable or your own logic.
        skip_index_creation = os.getenv("SKIP_INDEX_CREATION", "false").lower() == "true"
        if not skip_index_creation:
            self._create_indexes()

        # In dev, you may want to skip verifying the connection altogether,
        # or only do it if needed. 
        # For production, keep the verification with retries.
        if env == "production":
            self._verify_connection()

        self._initialized = True

    def _create_indexes(self):
        """
        Create necessary indexes. In production, do NOT drop
        indexes unless explicitly set via DROP_INDEXES=true.
        """
        drop_indexes = os.getenv("DROP_INDEXES", "False").lower() == "true"

        try:
            # Example: remove documents with null IDs if needed
            self.users.delete_many({"id": None})

            if drop_indexes:
                logger.info("DROP_INDEXES is True. Dropping indexes before creating new ones.")
                self.users.drop_indexes()
                self.projects.drop_indexes()
                self.chats.drop_indexes()
                self.slack_installations.drop_indexes()
                self.community_repos.drop_indexes()
                self.nuanced_graphs.drop_indexes()
            else:
                logger.info("DROP_INDEXES is False. Ensuring indexes without dropping.")

            # ----- Projects Indexes -----
            self.projects.create_index([("user_id", ASCENDING)], background=True)
            self.projects.create_index(
                [("id", ASCENDING), ("user_id", ASCENDING)],
                unique=True,
                background=True
            )
            self.projects.create_index(
                [("api_project", ASCENDING), ("api_key_id", ASCENDING)],
                background=True,
                sparse=True
            )

            # ----- Chats Indexes -----
            self.chats.create_index(
                [("project_id", ASCENDING), ("user_id", ASCENDING)],
                background=True
            )
            self.chats.create_index(
                [("id", ASCENDING), ("project_id", ASCENDING), ("user_id", ASCENDING)],
                unique=True,
                background=True
            )
            self.chats.create_index([("updated_at", -1)], background=True)

            # ----- Users Indexes -----
            self.users.create_index(
                [("id", ASCENDING)],
                unique=True,
                background=True,
                partialFilterExpression={"id": {"$type": "string"}}
            )
            self.users.create_index(
                [("github_installation_id", ASCENDING)],
                background=True,
                sparse=True
            )
            self.users.create_index(
                [("slack_user_ids", ASCENDING)],
                background=True,
                sparse=True
            )

            # ----- Slack Installations Indexes -----
            self.slack_installations.create_index(
                [("team_id", ASCENDING)],
                unique=True,
                background=True
            )

            # ----- API Keys Indexes -----
            self.api_keys.create_index(
                [("user_id", ASCENDING)], background=True
            )
            self.api_keys.create_index(
                [("key", ASCENDING)], unique=True, background=True
            )
            self.api_keys.create_index(
                [("id", ASCENDING), ("user_id", ASCENDING)],
                unique=True,
                background=True
            )

            # ----- Community Repos Indexes -----
            self.community_repos.create_index(
                [("id", ASCENDING)],
                unique=True,
                background=True
            )
            self.community_repos.create_index(
                [("repo_url", ASCENDING)],
                unique=True,
                background=True
            )
            self.community_repos.create_index([("status", ASCENDING)], background=True)
            self.community_repos.create_index([("is_indexed", ASCENDING)], background=True)
            self.community_repos.create_index([("indexed_at", -1)], background=True)
            
            # ----- Nuanced Graphs Indexes -----
            self.nuanced_graphs.create_index(
                [("project_id", ASCENDING)],
                unique=True,
                background=True
            )
            self.nuanced_graphs.create_index([("updated_at", -1)], background=True)

            # Create indexes for data sources collection
            data_sources_indexes = [
                IndexModel([("project_id", ASCENDING)]),
                IndexModel([("user_id", ASCENDING)]),
                IndexModel([("url", ASCENDING)]),
                IndexModel([("status", ASCENDING)]),
                IndexModel([("source_type", ASCENDING)])
            ]
            
            self.client.nozomio.data_sources.create_indexes(data_sources_indexes)
            logger.info("Created indexes for data_sources collection")
            
            # Create indexes for project-source associations
            project_sources_indexes = [
                IndexModel([("project_id", ASCENDING)]),
                IndexModel([("source_id", ASCENDING)]),
                IndexModel([("project_id", ASCENDING), ("source_id", ASCENDING)], unique=True)
            ]
            
            self.client.nozomio.project_sources.create_indexes(project_sources_indexes)
            logger.info("Created indexes for project_sources collection")

            logger.info("Successfully created/ensured MongoDB indexes.")
        except OperationFailure as e:
            logger.error(f"Failed to create indexes: {e}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    def _verify_connection(self):
        """Verify MongoDB connection with retry logic."""
        try:
            self._client.admin.command('ping')
            logger.info("Successfully connected to MongoDB.")
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    @property
    def client(self) -> MongoClient:
        """Expose the raw MongoClient if needed."""
        return self._client

    def close(self):
        """Close MongoDB connection gracefully."""
        if self._client:
            self._client.close()
            logger.info("MongoDB connection closed.")

    # Data Sources methods
    async def create_data_source(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new data source.
        
        Args:
            data: Dictionary containing data source information
            
        Returns:
            Newly created data source document
        """
        try:
            # Generate a unique ID if not provided
            if "id" not in data:
                data["id"] = str(uuid.uuid4())
                
            # Add timestamps
            now = datetime.utcnow().isoformat()
            data["created_at"] = now
            data["updated_at"] = now
            
            # Set default status if not provided
            if "status" not in data:
                data["status"] = "pending"
                
            # Set is_active flag (default to True for new sources)
            if "is_active" not in data:
                data["is_active"] = True
                
            # Insert the document - no await for synchronous operation
            result = self.client.nozomio.data_sources.insert_one(data)
            
            if result.inserted_id:
                return data
            else:
                return None
        except Exception as e:
            logger.error(f"Error creating data source: {e}")
            return None
    
    def get_data_source_by_id(self, source_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a data source by its ID.
        
        Args:
            source_id: ID of the data source to retrieve
            
        Returns:
            Data source document or None if not found
        """
        try:
            # Use find_one directly for synchronous operation
            data_source = self.client.nozomio.data_sources.find_one({"id": source_id})
            return data_source
        except Exception as e:
            logger.error(f"Error getting data source {source_id}: {e}")
            return None
    
    def list_data_sources(self, project_id: Optional[str] = None, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all data sources, optionally filtered by project ID and user ID.
        
        Args:
            project_id: Optional project ID to filter sources
            user_id: Optional user ID to filter sources (for data isolation)
            
        Returns:
            List of data source documents
        """
        try:
            query = {}
            if project_id:
                query["project_id"] = project_id
            if user_id:
                query["user_id"] = user_id
                
            # For synchronous MongoDB driver, convert cursor to list directly
            cursor = self.client.nozomio.data_sources.find(query)
            return list(cursor)
        except Exception as e:
            logger.error(f"Error listing data sources: {e}")
            return []
    
    def get_active_data_sources(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all active data sources regardless of project.
        
        Args:
            user_id: Optional user ID to filter sources (for data isolation)
            
        Returns:
            List of active data source documents
        """
        try:
            # For synchronous MongoDB driver, convert cursor to list directly
            query = {"is_active": True}
            if user_id:
                query["user_id"] = user_id
                
            cursor = self.client.nozomio.data_sources.find(query)
            return list(cursor)
        except Exception as e:
            logger.error(f"Error getting active data sources: {e}")
            return []
    
    async def update_data_source(self, source_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing data source.
        
        Args:
            source_id: ID of the data source to update
            updates: Dictionary containing fields to update
            
        Returns:
            Updated data source document
        """
        try:
            # Add updated timestamp
            updates["updated_at"] = datetime.utcnow().isoformat()
            
            # Update the document - use synchronous operation
            result = self.client.nozomio.data_sources.update_one(
                {"id": source_id},
                {"$set": updates}
            )
            
            if result.modified_count > 0 or result.matched_count > 0:
                # Get and return the updated document - retrieve directly
                return self.client.nozomio.data_sources.find_one({"id": source_id})
            else:
                logger.warning(f"No data source found with ID: {source_id}")
                return None
        except Exception as e:
            logger.error(f"Error updating data source: {e}")
            return None

    async def toggle_data_source_active_status(self, source_id: str, is_active: bool) -> Optional[Dict[str, Any]]:
        """
        Toggle the active status of a data source.
        
        Args:
            source_id: ID of the data source to update
            is_active: Boolean indicating whether the source should be active
            
        Returns:
            Updated data source document
        """
        try:
            # Use this method to ensure we have consistent behavior
            updates = {"is_active": is_active}
            
            # Add updated timestamp
            updates["updated_at"] = datetime.utcnow().isoformat()
            
            # Update the document
            result = self.client.nozomio.data_sources.update_one(
                {"id": source_id},
                {"$set": updates}
            )
            
            if result.modified_count > 0 or result.matched_count > 0:
                # Get the updated document
                updated_doc = self.client.nozomio.data_sources.find_one({"id": source_id})
                if updated_doc:
                    logger.info(f"Successfully updated data source {source_id} active status to {is_active}")
                    return updated_doc
                else:
                    logger.warning(f"Updated data source {source_id} but couldn't retrieve it")
                    return None
            else:
                logger.warning(f"No data source found with ID: {source_id}")
                return None
        except Exception as e:
            logger.error(f"Error toggling data source active status: {e}")
            return None
    
    async def delete_data_source(self, source_id: str) -> bool:
        """
        Delete a data source.
        
        Args:
            source_id: The ID of the data source to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            result = self.client.nozomio.data_sources.delete_one({"id": source_id})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting data source {source_id}: {e}")
            raise

    async def associate_data_source_with_project(self, project_id: str, source_id: str) -> bool:
        """
        Associate a data source with a project.
        
        Args:
            project_id: ID of the project
            source_id: ID of the data source
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if project exists
            project = self.client.nozomio.projects.find_one({"id": project_id})
            if not project:
                logger.warning(f"Project {project_id} not found")
                return False
                
            # Check if data source exists
            data_source = self.client.nozomio.data_sources.find_one({"id": source_id})
            if not data_source:
                logger.warning(f"Data source {source_id} not found")
                return False
                
            # Create or update association
            result = self.client.nozomio.project_sources.update_one(
                {"project_id": project_id, "source_id": source_id},
                {"$set": {"project_id": project_id, "source_id": source_id}},
                upsert=True
            )
            
            return result.modified_count > 0 or result.upserted_id is not None
        except Exception as e:
            logger.error(f"Error associating data source with project: {e}")
            return False
            
    async def disassociate_data_source_from_project(self, project_id: str, source_id: str) -> bool:
        """
        Remove association between a data source and a project.
        
        Args:
            project_id: ID of the project
            source_id: ID of the data source
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Delete the association
            result = self.client.nozomio.project_sources.delete_one({
                "project_id": project_id,
                "source_id": source_id
            })
            
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error removing data source from project: {e}")
            return False
    
    def get_associated_data_sources(self, project_id: str) -> List[str]:
        """
        Get all data source IDs associated with a project.
        
        Args:
            project_id: ID of the project
            
        Returns:
            List of data source IDs
        """
        try:
            # Find all associations for this project
            associations = list(self.client.nozomio.project_sources.find({"project_id": project_id}))

            # Extract source IDs
            source_ids = [assoc["source_id"] for assoc in associations]
            
            return source_ids
        except Exception as e:
            logger.error(f"Error getting associated data sources: {e}")
            return []
            
    def get_projects_for_data_source(self, source_id: str) -> List[str]:
        """
        Get all project IDs associated with a data source.
        
        Args:
            source_id: ID of the data source
            
        Returns:
            List of project IDs
        """
        try:
            # Find all associations for this source
            associations = list(self.client.nozomio.project_sources.find({"source_id": source_id}))
            
            # Extract project IDs
            project_ids = [assoc["project_id"] for assoc in associations]
            
            return project_ids
        except Exception as e:
            logger.error(f"Error getting projects for data source: {e}")
            return []
            
    def update_data_source_sync(self, source_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Synchronous version of update_data_source for use in Celery tasks.
        
        Args:
            source_id: ID of the data source to update
            updates: Dictionary containing fields to update
            
        Returns:
            Updated data source document or None if operation failed
        """
        try:
            # Add updated timestamp if not provided
            if "updated_at" not in updates:
                updates["updated_at"] = datetime.utcnow().isoformat()
            
            # Update the document
            result = self.client.nozomio.data_sources.update_one(
                {"id": source_id},
                {"$set": updates}
            )
            
            if result.modified_count > 0 or result.matched_count > 0:
                # Get and return updated document
                return self.client.nozomio.data_sources.find_one({"id": source_id})
            else:
                logger.warning(f"No data source found with ID: {source_id}")
                return None
        except Exception as e:
            logger.error(f"Error updating data source synchronously: {e}")
            return None
    
    def find_projects(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find projects matching the given query.
        
        Args:
            query: MongoDB query document
            
        Returns:
            List of matching project documents
        """
        try:
            # PyMongo find() returns a cursor, not an awaitable
            cursor = self.projects.find(query)
            result = []
            for doc in cursor:
                result.append(doc)
            return result
        except Exception as e:
            logger.error(f"Error finding projects: {e}")
            return []
    
    def find_data_sources(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find data sources matching the given query.
        
        Args:
            query: MongoDB query document
            
        Returns:
            List of matching data source documents
        """
        try:
            # PyMongo find() returns a cursor, not an awaitable
            cursor = self.client.nozomio.data_sources.find(query)
            result = []
            for doc in cursor:
                result.append(doc)
            return result
        except Exception as e:
            logger.error(f"Error finding data sources: {e}")
            return []
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the MongoDB connection.
        
        Returns:
            Health status dictionary
        """
        try:
            # Run serverStatus command to check DB health
            self.client.admin.command("ping")
            status = self.client.admin.command("serverStatus")
            
            return {
                "status": "healthy",
                "connections": status.get("connections", {}).get("current", 0),
                "timestamp": datetime.utcnow().isoformat()
            }
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Database health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Unexpected error in database health check: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

# Global instance
db = MongoDB()
