# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: April 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

# =============== // STANDARD IMPORT // ===============

import time
import signal
import threading
from pathlib import Path
import functools

# =============== // LIBRARY IMPORT // ===============

from loguru import logger
import schedule

# =============== // MODULE IMPORT // ===============

import constants as c
from modules.utils.log_setup import setup_debug_log

# =============== // LOGGER SETUP // ===============

LOG_DIR: Path = c.LOG_DIR / "scheduler"
LOG_DIR.mkdir(parents=True, exist_ok=True)

setup_debug_log(
    logger=logger,
    dir=LOG_DIR
)

logger.info("Starting Scheduler! 🚀")

# =============== // HELPER FUNCTIONS // ===============

THREADS: list[threading.Thread] = []
SHUTDOWN_EVENT: threading.Event = threading.Event()


def catch_exceptions(cancel_on_failure=False):
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except Exception as e:
                import traceback
                logger.error(e)
                logger.error(traceback.format_exc())
                if cancel_on_failure:
                    return schedule.CancelJob
        return wrapper
    return catch_exceptions_decorator


def run_job_in_background(job_func, *args, cancel_on_failure=False, **kwargs):
    @catch_exceptions(cancel_on_failure=cancel_on_failure)
    def job_wrapper():
        logger.info(f"Starting job: {job_func.__name__}")
        job_func(*args, **kwargs)
        logger.info(f"Finished job: {job_func.__name__}")

    thread = threading.Thread(target=job_wrapper, daemon=True, name=job_func.__name__)
    THREADS.append(thread)
    thread.start()
    logger.info(f"Started thread for job: {job_func.__name__}")


def shutdown():
    logger.info("Shutdown initiated. Signaling all threads to stop...")
    SHUTDOWN_EVENT.set()

    for thread in THREADS:
        logger.info(f"Waiting for thread {thread.name} to finish...")
        thread.join(timeout=30)
        if thread.is_alive():
            logger.warning(f"Thread {thread.name} did not finish in time.")

    logger.info("All threads have been handled. Shutdown complete.")
    exit(0)


# =============== // SIGNAL HANDLER // ===============

def handler(signum, frame):
    sig_name: str = signal.Signals(signum).name
    logger.warning(f"Received {sig_name} signal. Shutting down gracefully...")
    shutdown()


signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)

# =============== // JOB SCHEDULES // ===============


def sample_job():
    logger.info("Sample job is running...")
    import time
    time.sleep(5)
    logger.info("Sample job done.")


schedule.every(20).seconds.do(lambda: run_job_in_background(sample_job))


while True:
    schedule.run_pending()
    time.sleep(1)
