import time
import os
import random
import math
import logging
import queue
import random
from multiprocessing import current_process
from datetime import datetime


logger = logging.getLogger("demo.consumer")

processing_time = 0.01   # 10 milliseconds

def do_something(item):
    # sleeping is also work :)
    time.sleep(processing_time)
    return f" {item} - {datetime.now()}"


# The consumer function takes data off of the Queue
def process_items(prod_queue, result_queue):
    while True: 
        try:
            item = prod_queue.get(timeout=2)
            logger.debug(f"Item {item} picked from the prod_queue")
            result = do_something(item)
            result_queue.put(result)
            logger.debug(f"Result {result} put into result_queue")
        except queue.Empty:
            logger.debug(f"Intput queue (prod_queue) is empty. Process {current_process().name} exists.")
            break
