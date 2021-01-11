import time
import os
import random
import sys
import multiprocessing as mp
import queue
import logging
import timeit

import consume.consumer as consumer
import produce.producer as producer
    


# producer queue
prod_queue = mp.Queue()

# multi consumer result queue
result_queue = mp.Queue()



def with_multiprocessing(num_procs):
    start_time = timeit.default_timer()
    
    logger.debug("Starting producer process")
    producer_proc = mp.Process(target=producer.produce_items, 
                          args=(prod_queue,), 
                          name="producer_proc",
                          daemon=True)
    producer_proc.start()
    logger.debug("Producer process started")

    logger.debug("Strarting consumer processes")
    count = 1
    consumer_procs = []
    for i in range(num_procs):
        consumer_proc = mp.Process(target=consumer.process_items,
                                args=(prod_queue, result_queue, ),
                                name=f"consumer_proc_{i}",
                                daemon=True)
        consumer_proc.start()
        consumer_procs.append(consumer_proc)

    logger.debug("All consumer processes started")

    while True: 
        try: 
            logger.debug(f"Getting result from result_queue. Count: {count}")
            result = result_queue.get(timeout=5)
            count += 1
            if count == producer.num_items:
                logger.debug("All items processed. Quitting the picking loop.")
                break
        except queue.Empty:
            logger.debug("Worker processes result queue (result_queue) is empty. Stop picking results")
            break

    duration = timeit.default_timer() - start_time

    logger.debug("Waiting for consumer processes to quit")
    for proc in consumer_procs: 
        logger.debug(f"Joining process: {proc.name}")
        proc.join()

    return duration


def config_logging():
    logger = logging.getLogger("demo")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s:%(lineno)d - %(funcName)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    return logger


if __name__ == '__main__':
    config_logging()
    logger = logging.getLogger("demo")

    logger.setLevel(logging.INFO)

    num_procs = 1    # ~12 sec
    # num_procs = 2    # ~6 sec
    duration = with_multiprocessing(num_procs)
    logger.info(f"It took {duration} seconds with {num_procs} processes")
