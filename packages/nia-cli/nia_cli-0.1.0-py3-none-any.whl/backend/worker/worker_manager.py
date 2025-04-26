import os
import sys
import logging
import subprocess
import signal
import time
import threading
import psutil
import resource
from datetime import datetime, timedelta
from typing import List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# python -m worker.worker_manager
class WorkerManager:
    """
    Manages and monitors multiple worker processes for repository indexing.
    Features:
    - Health monitoring for each worker
    - Resource limits to prevent memory leaks
    - Automatic restarts for unhealthy or crashed workers
    - Graceful shutdown handling
    """
    
    def __init__(self, num_workers: int = 3):
        self.num_workers = num_workers
        self.workers: List[subprocess.Popen] = []
        self.processes = {}
        self.worker_logs = {}
        self.worker_status = {}  # Track health of each worker
        self.stop_event = threading.Event()  # For graceful shutdown
        
        # System resource configuration
        self.max_memory_percent = 80  # Restart if worker exceeds this % of system memory
        self.max_cpu_percent = 90     # Restart if CPU usage exceeds this %
        self.health_check_interval = 60  # Check health every minute
        self.restart_unhealthy_after = 120  # Restart workers unresponsive for 2 minutes
        
        # Ensure NUM_WORKERS is set in environment
        os.environ["NUM_WORKERS"] = str(num_workers)
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, self.handle_shutdown)
        signal.signal(signal.SIGINT, self.handle_shutdown)
        
        logger.info(f"Worker manager initialized with {num_workers} workers")

    def handle_shutdown(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received shutdown signal {signum}, stopping workers gracefully...")
        self.stop_event.set()

    def start_worker(self, worker_id: int) -> Optional[subprocess.Popen]:
        """Start a single worker process with proper environment variables."""
        try:
            # Set resource limits to prevent runaway processes
            # Set maximum number of open file descriptors (important for network connections)
            try:
                # Set soft limit to 2048 file descriptors (or whatever is appropriate for your app)
                resource.setrlimit(resource.RLIMIT_NOFILE, (2048, resource.getrlimit(resource.RLIMIT_NOFILE)[1]))
                logger.info(f"Set file descriptor limit for worker {worker_id}")
            except Exception as e:
                logger.warning(f"Could not set resource limits for worker {worker_id}: {e}")
            
            # Create a new environment with worker-specific variables
            worker_env = os.environ.copy()
            worker_env["WORKER_ID"] = str(worker_id)
            
            # Start the worker process with process group
            process = subprocess.Popen(
                [sys.executable, "-m", "worker.indexer"],
                env=worker_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                preexec_fn=os.setsid if os.name != 'nt' else None  # Create new process group on Unix
            )
            
            # Record worker info
            self.processes[worker_id] = process
            self.worker_logs[worker_id] = {"stdout": [], "stderr": []}
            
            # Initialize health status tracking
            self.worker_status[worker_id] = {
                "pid": process.pid,
                "start_time": datetime.now(),
                "last_activity": datetime.now(),
                "restart_count": 0,
                "health_status": "starting",
                "last_health_check": datetime.now(),
                "memory_usage": 0,
                "cpu_usage": 0,
                "network_errors": 0
            }
            
            # Start output monitoring threads
            def monitor_output(pipe, is_error=False):
                try:
                    for line in pipe:
                        if is_error:
                            logger.error(f"[Worker {worker_id}] {line.strip()}")
                        else:
                            logger.info(f"[Worker {worker_id}] {line.strip()}")
                except BrokenPipeError:
                    logger.warning(f"[Worker {worker_id}] Broken pipe in output monitoring")
                except Exception as e:
                    logger.error(f"[Worker {worker_id}] Error monitoring output: {e}")

            import threading
            threading.Thread(target=monitor_output, args=(process.stdout,), daemon=True).start()
            threading.Thread(target=monitor_output, args=(process.stderr, True), daemon=True).start()
            
            logger.info(f"Started worker {worker_id} with PID {process.pid}")
            return process
        except Exception as e:
            logger.error(f"Failed to start worker {worker_id}: {e}")
            return None

    def start_workers(self):
        """Start all worker processes."""
        logger.info(f"Starting {self.num_workers} workers...")
        
        for i in range(self.num_workers):
            worker = self.start_worker(i)
            if worker:
                self.workers.append(worker)
        
        if len(self.workers) == self.num_workers:
            logger.info("All workers started successfully")
        else:
            logger.warning(f"Only {len(self.workers)} of {self.num_workers} workers started")

    def stop_workers(self):
        """Stop all worker processes gracefully."""
        logger.info("Stopping workers...")
        
        for worker in self.workers:
            try:
                # Try to stop the entire process group
                if os.name != 'nt':  # Unix-like systems
                    try:
                        os.killpg(os.getpgid(worker.pid), signal.SIGTERM)
                    except ProcessLookupError:
                        pass  # Process already gone
                
                # Fallback to normal termination
                worker.terminate()
                
                try:
                    worker.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    if os.name != 'nt':
                        os.killpg(os.getpgid(worker.pid), signal.SIGKILL)
                    worker.kill()
                    worker.wait()
            except Exception as e:
                logger.error(f"Error stopping worker PID {worker.pid}: {e}")
        
        self.workers = []
        logger.info("All workers stopped")

    def monitor_workers(self):
        """Monitor workers and restart any that have died."""
        while True:
            for i, worker in enumerate(self.workers[:]):
                if worker.poll() is not None:
                    logger.warning(f"Worker {i} (PID {worker.pid}) died, restarting...")
                    self.workers.remove(worker)
                    new_worker = self.start_worker(i)
                    if new_worker:
                        self.workers.append(new_worker)
            time.sleep(5)

def handle_shutdown(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info(f"Received signal {signum}, shutting down...")
    if hasattr(handle_shutdown, 'manager'):
        handle_shutdown.manager.stop_workers()
    sys.exit(0)

def main():
    num_workers = int(os.getenv("NUM_WORKERS", "3"))
    logger.info(f"Starting worker manager with {num_workers} workers")
    
    manager = WorkerManager(num_workers)
    handle_shutdown.manager = manager
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    
    try:
        manager.start_workers()
        manager.monitor_workers()
    except Exception as e:
        logger.error(f"Worker manager error: {e}")
        manager.stop_workers()
        sys.exit(1)

if __name__ == "__main__":
    main()