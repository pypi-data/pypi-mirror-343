#!/usr/bin/env python3
"""
Hatchet Worker for NIA App
Replaces the Celery worker with Hatchet-based distributed task execution.
"""
import os
import sys
import logging
import signal
from hatchet_sdk import Hatchet

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
)
logger = logging.getLogger("hatchet.worker")

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

def setup_signal_handlers(worker):
    """Set up graceful shutdown handlers"""
    def shutdown_handler(signum, frame):
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        worker.close()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

def main():
    """Main entry point for the Hatchet worker"""
    # Get worker ID from environment or generate one
    worker_id = os.getenv("WORKER_ID", f"worker-{os.getpid()}")
    max_runs = int(os.getenv("MAX_CONCURRENT_RUNS", "2"))
    
    logger.info(f"Starting Hatchet worker {worker_id} with {max_runs} max concurrent runs")
    
    try:
        # Initialize Hatchet client
        hatchet = Hatchet()
        
        # Create worker
        worker = hatchet.worker(
            name=f"nia-{worker_id}",
            max_runs=max_runs
        )
        
        # Set up signal handlers for graceful shutdown
        setup_signal_handlers(worker)
        
        # Import workflows - these imports will register the workflows with Hatchet
        logger.info("Importing workflows...")
        from workflows.indexing import IndexRepositoryWorkflow, WebIndexingWorkflow
        from workflows.maintenance import CleanupStaleJobsWorkflow, HealthCheckWorkflow
        
        # Register workflow instances with the worker
        logger.info("Registering workflows with worker...")
        worker.register_workflow(IndexRepositoryWorkflow())
        worker.register_workflow(WebIndexingWorkflow())
        worker.register_workflow(CleanupStaleJobsWorkflow())
        worker.register_workflow(HealthCheckWorkflow())
        
        # Start worker (blocking call)
        logger.info(f"Starting Hatchet worker {worker_id}...")
        worker.start()
        
    except Exception as e:
        logger.error(f"Error in Hatchet worker: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()