import os
import sys
import logging
from datetime import datetime, timedelta
from hatchet_sdk import Hatchet, Context, sync_to_async

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
)
logger = logging.getLogger("workflows.maintenance")

# Initialize Hatchet client
hatchet = Hatchet()

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import required modules
from db import MongoDB
from db_helpers import find_stale_data_sources, find_stale_projects, perform_health_check, update_project_async, sync_to_async_project_update
from workflows.utils import handle_workflow_errors

# Initialize MongoDB
db = MongoDB()

@hatchet.workflow(on_crons=["*/30 * * * *"])  # Run every 30 minutes
class CleanupStaleJobsWorkflow:
    """
    Workflow to cleanup stale jobs that may be stuck.
    Replaces the Celery periodic task 'worker.tasks.cleanup_stale_jobs'
    """
    
    @hatchet.step()
    @handle_workflow_errors
    async def cleanup_stale_jobs(self, context: Context):
        """Find and mark stale jobs as failed"""
        logger.info("Running stale job cleanup")
        
        # Define stale threshold (3 hours)
        stale_threshold = datetime.now() - timedelta(hours=3)
        stale_projects = []
        stale_sources = []
        
        try:
            # Find projects stuck in "indexing" state - using sync method
            stale_projects = find_stale_projects("indexing", stale_threshold)
        except Exception as e:
            logger.error(f"Error finding projects: {e}")
            stale_projects = []
        
        # Update stale projects to error state
        for project in stale_projects:
            project_id = project.get("id")
            user_id = project.get("user_id")
            if project_id and user_id:
                try:
                    # Use sync_to_async_project_update to handle the update
                    update_result = sync_to_async_project_update(
                        project_id=project_id,
                        user_id=user_id,
                        status="error",
                        error="Indexing timed out after 3 hours",
                        details={
                            "stage": "timeout",
                            "message": "Indexing process timed out",
                            "cleaned_up_at": datetime.now().isoformat()
                        }
                    )
                    logger.info(f"Marked stale project {project_id} as failed: {update_result}")
                except Exception as e:
                    logger.error(f"Error updating stale project {project_id}: {e}")
        
        try:
            # Find data sources stuck in "processing" state - using sync method
            stale_sources = find_stale_data_sources(db, "processing", stale_threshold)
        except Exception as e:
            logger.error(f"Error finding data sources: {e}")
            stale_sources = []
        
        # Update stale data sources to error state
        for source in stale_sources:
            source_id = source.get("id")
            if source_id:
                try:
                    # We still await this method since it's defined as async
                    await db.update_data_source(
                        source_id=source_id,
                        updates={
                            "status": "error",
                            "error": "Processing timed out after 3 hours"
                        }
                    )
                    logger.info(f"Marked stale data source {source_id} as failed")
                except Exception as e:
                    logger.error(f"Error updating stale data source {source_id}: {e}")
        
        logger.info(f"Found {len(stale_projects)} stale projects and {len(stale_sources)} stale data sources")
        
        return {
            "stale_projects_count": len(stale_projects),
            "stale_sources_count": len(stale_sources),
            "timestamp": datetime.now().isoformat()
        }

@hatchet.workflow(on_crons=["0 * * * *"])  # Run every hour
class HealthCheckWorkflow:
    """
    Workflow to run health checks on the system.
    """
    
    @hatchet.step()
    @handle_workflow_errors
    async def check_system_health(self, context: Context):
        """Check overall system health"""
        logger.info("Running system health check")
        
        health_status = {
            "status": "healthy",
            "checks": {},
            "timestamp": datetime.now().isoformat()
        }
        
        # Check MongoDB connection - using sync method
        try:
            db_health = perform_health_check(db)
            health_status["checks"]["mongodb"] = db_health
        except Exception as e:
            logger.error(f"Health check mongodb failed: {{'status': 'error', 'error': '{str(e)}', 'timestamp': '{datetime.now().isoformat()}'}}")
            health_status["checks"]["mongodb"] = {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        
        # Check Hatchet status - to be implemented if needed
        health_status["checks"]["hatchet"] = {"status": "healthy", "message": "Workflow running"}
        
        # Check if any other health checks are unhealthy
        for check_name, check_result in health_status["checks"].items():
            if check_result.get("status") != "healthy":
                health_status["status"] = "unhealthy"
                logger.error(f"Health check {check_name} failed: {check_result}")
        
        logger.info(f"System health check completed with status: {health_status['status']}")
        return health_status