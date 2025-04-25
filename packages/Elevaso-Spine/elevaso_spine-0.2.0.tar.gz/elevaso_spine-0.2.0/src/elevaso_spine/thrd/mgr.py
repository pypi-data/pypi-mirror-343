"""
.. module:: mgr
    :platform: Unix, Windows
    :synopsis: Function to manage threads
"""

# Python Standard Libraries
import logging
import queue
import time

# 3rd Party Libraries


# Project Specific Libraries


LOGGER = logging.getLogger(__name__)


def create(
    threads: int,
    thread_class: object,
    params: dict,
    thread_queue: queue.Queue = None,
) -> list:
    """Create threads for parallel processing

    Args:
        threads (int): Number of threads to create

        thread_class (object): Thread class to create

        params (dict): Dictionary of parameters to pass into thread

        thread_queue (queue.Queue, Optional): Queue to retrieve items to work,
        defaults to None

    Raises:
        ValueError if threads == 0

    Returns:
        list: List of thread objects created
    """
    if threads == 0:
        raise ValueError("Threads must be greater than 0")

    thread_list = []

    class_name = thread_class.__name__

    for enum in range(threads):
        LOGGER.debug(
            "Creating %(class_name)s thread %(enum)s",
            {"enum": enum, "class_name": class_name},
        )

        if thread_queue:
            thread = thread_class(
                worker_queue=thread_queue, thread_num=enum, **params
            )
        else:
            thread = thread_class(thread_num=enum, **params)

        thread.daemon = True
        thread_list.append(thread)
        thread.start()

    LOGGER.info(
        "Created %(thread_list_len)s %(class_name)s thread(s)",
        {"thread_list_len": len(thread_list), "class_name": class_name},
    )

    return thread_list


def has_working_thread(thread_list: list) -> bool:
    """Checks if there are threads still alive

    Args:
        thread_list (list): List of thread objects

    Returns:
        bool: True/False if has at least one thread alive
    """
    for thread in thread_list:
        if thread.is_alive():
            return True

    return False


# pylint: disable=unsubscriptable-object
def thread_metrics(thread_list: list) -> tuple[int, int, int]:
    """Retrieves built-in metrics from all threads

    Args:
        thread_list (list): List of thread objects

    Returns:
        tuple: Containing
            rows_processed: Number of queue records processed for all threads
            rows_errored: Number of queue records errored for all threads
            threads: Number of threads
    """
    return (
        sum([thread.rows_processed for thread in thread_list]),
        sum([thread.rows_errored for thread in thread_list]),
        len(thread_list),
    )


def wait_queue_empty(
    thread_queue: queue.Queue, thread_list: list, interval: int = 5
):
    """Check if a queue is empty and outputs logging messages, additionally
    checks if there are threads alive to prevent waiting for a queue to finish
    if all worker threads have stopped

    Args:
        thread_queue (queue.Queue): Queue to check for empty status

        thread_list (list): List of threads working the queue

        interval (int, Optional): Interval in seconds to print queue depth,
        defaults to 5

        .. note::

            If set to 0, the queue will not be actively checked while printing
            status message, instead it will wait until the queue is empty
            through the queue.join() function

    Raises:
        Exception: If queue is not empty and no working threads in thread_list
    """
    if interval > 0:
        __wait(thread_queue, thread_list, interval)

    thread_queue.join()


def __wait(thread_queue: queue.Queue, thread_list: list, interval: int = 5):
    """Loop until queue is empty

    Args:
        thread_queue (queue.Queue): Queue to check for empty status

        thread_list (list): List of threads working the queue

        interval (int, Optional): Interval in seconds to print queue depth,
        defaults to 5

        .. note::

            If set to 0, the queue will not be actively checked while printing
            status message, instead it will wait until the queue is empty
            through the queue.join() function

    Raises:
        Exception: If queue is not empty and no working threads in thread_list
    """
    i = 0

    while not thread_queue.empty():
        time.sleep(1)

        if has_working_thread(thread_list):
            i += 1

            __log_size(i, interval, thread_queue.qsize())
        else:
            raise Exception(
                f"{thread_queue.qsize()} records in queue with no active "
                "threads"
            )


def __log_size(i: int, interval: int, q_size: int):
    """Log the current size of queue if interval matches

    Args:
        i (int): Current second

        interval (int): Interval at which to print

        q_size (int): Current queue size
    """
    if i == interval:
        LOGGER.info("%(q_size)s Records in Queue", {"q_size": q_size})
        i = 0
