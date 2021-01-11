import time
import os
import random
import logging

logger = logging.getLogger("demo.producer")

# num_items = 34
num_items = 1000

# Producer function that places data on the Queue
def produce_items(prod_queue):
    logger.debug("Producer process ... ")

    items = []
    for i in range(num_items):
        items.append(f"item_{i}")

    for item in items:
        # time.sleep(random.randint(0, 2))
        prod_queue.put(item)
        logger.debug(f"{item} added to the queue")
