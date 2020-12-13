



# ---------------------------------------------
#
# Semaphore
# A Semaphore is a counter with atomic counting: it is guaranteed that the operating system 
# will not swap out the thread in the middle of incrementing or decrementing the counter.

# The internal counter is "decremented" when you call .acquire() and "incremented" when 
# you call .release(). 
# If a thread calls .acquire() when the counter is zero, that thread will block until a 
# different thread calls .release() and increments the counter to one.

# Semaphores are frequently used to protect a resource that has a limited capacity. 
# An example would be if you have a pool of connections and want to limit the size of that 
# pool to a specific number.

# ---------------------------------------------
#
# Timer
# A threading.Timer is a way to schedule a function to be called after a certain 
# amount of time has passed. You create a Timer by passing in a number of seconds 
# to wait and a function to call:

# t = threading.Timer(30.0, my_function)

# You start the Timer by calling .start(). The function will be called on a new thread 
# at some point after the specified time, but be aware that there is no promise that 
# it will be called exactly at the time you want.

# If you want to stop a Timer that you’ve already started, you can cancel it by calling 
# .cancel(). Calling .cancel() after the Timer has triggered does nothing and does not 
# produce an exception.

# A Timer can be used to prompt a user for action after a specific amount of time. 
# If the user does the action before the Timer expires, .cancel() can be called.

# ---------------------------------------------
#
# Barrier
# A threading.Barrier can be used to keep a fixed number of threads in sync. When creating 
# a Barrier, the caller must specify how many threads will be synchronizing on it. Each 
# thread calls .wait() on the Barrier. They all will remain blocked until the specified 
# number of threads are waiting, and then the are all released at the same time.

# Remember that threads are scheduled by the operating system so, even though all of the 
# threads are released simultaneously, they will be scheduled to run one at a time.

# One use for a Barrier is to allow a pool of threads to initialize themselves. Having the 
# threads wait on a Barrier after they are initialized will ensure that none of the threads 
# start running before all of the threads are finished with their initialization.
#
#
# ---------------------------------------------




# ================================================
#
# import concurrent.futures
# import logging
# import queue
# import random
# import threading
# import time


# def producer(queue, event):
#     """Pretend we're getting a number from the network."""
#     while not event.is_set():
#         time.sleep(random.uniform(0, 0.05))
#         message = random.randint(1, 101)
#         logging.info("Producer produced and will add message: %s", message)
#         queue.put(message)

#     logging.info("Producer received event. Exiting")


# def consumer(queue, event):
#     """Pretend we're saving a number in the database."""
#     while not event.is_set() or not queue.empty():
#         time.sleep(random.uniform(0, 0.05))
#         message = queue.get()
#         logging.info(
#             "Consumer consuming message: %s (size=%d)", message, queue.qsize()
#         )

#     logging.info("Consumer received event. Exiting")


# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")

#     pipeline = queue.Queue(maxsize=10)
#     event = threading.Event()
#     with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#         executor.submit(producer, pipeline, event)
#         executor.submit(consumer, pipeline, event)

#         time.sleep(1)
#         logging.info("Main: about to set event")
#         event.set()



# =================================================
#
# import logging
# import threading
# import time
# import concurrent.futures
# import random 
# import copy
# import queue 



# def producer(pipeline, event):
#     """Pretend we're getting a number from the network."""
#     while not event.is_set():
#         message = random.randint(1, 101)
#         logging.info("Producer got message: %s", message)
#         pipeline.set_message(message, "Producer")

#     logging.info("Producer received EXIT event. Exiting")


# def consumer(pipeline, event):
#     """Pretend we're saving a number in the database."""

#     # Not making sure the queue is empty before the consumer finishes creates two issues. 
#     # firstly, losing the final messages; but the more serious one is that the producer 
#     # can get caught attempting to add a message to a full queue and never return.
#     # This happens if the event gets triggered after the producer has checked the .is_set() 
#     # condition but before it calls pipeline.set_message().
#     # If that happens, it’s possible for the producer to wake up and exit with the queue 
#     # still completely full. The producer will then call .set_message() which will wait 
#     # until there is space on the queue for the new message. The consumer has already exited, 
#     # so this will not happen and the producer will not exit.
#     while not event.is_set() or not pipeline.empty():
#         message = pipeline.get_message("Consumer")
#         logging.info("Consumer storing message: %s  (queue size=%s)", message, pipeline.qsize())

#     logging.info("Consumer received EXIT event. Exiting")


# class Pipeline(queue.Queue):
#     def __init__(self):
#         super().__init__(maxsize=10)

#     def get_message(self, name):
#         logging.debug("%s:about to get from queue", name)
#         value = self.get()
#         logging.debug("%s:got %d from queue", name, value)
#         return value

#     def set_message(self, value, name):
#         logging.debug("%s:about to add %d to queue", name, value)
#         self.put(value)
#         logging.debug("%s:added %d to queue", name, value)


# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#     logging.getLogger().setLevel(logging.DEBUG)

#     pipeline = Pipeline()
#     event = threading.Event()
#     with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#         executor.submit(producer, pipeline, event)
#         executor.submit(consumer, pipeline, event)

#         time.sleep(0.1)
#         logging.info("Main: about to set event")
#         event.set()




# ==========================================
#
# import logging
# import threading
# import time
# import concurrent.futures
# import random 
# import copy


# SENTINEL = "STOP"


# def producer(pipeline):
#     """Pretend we're getting a message from the network."""
#     for index in range(10):
#         message = random.randint(1, 101)
#         logging.info("Producer produced and will set message: %s", message)
#         pipeline.set_message(message, "Producer")

#     # Send a sentinel message to tell consumer we're done
#     pipeline.set_message(SENTINEL, "Producer")


# def consumer(pipeline):
#     """Pretend we're saving a number in the database."""
#     message = 0
#     while message is not SENTINEL:
#         message = pipeline.get_message("Consumer")
#         if message is not SENTINEL:
#             logging.info("Consumer consuming message: %s", message)


# class Pipeline:
#     """
#     Class to allow a single element pipeline between producer and consumer.

#     .message stores the message to pass.
    
#     .producer_lock is a threading.Lock object that restricts access 
#      to the message by the producer thread.
    
#     .consumer_lock is also a threading.Lock that restricts access 
#      to the message by the consumer thread.
#     """
#     def __init__(self):
#         self.message = 0
#         self.producer_lock = threading.Lock()
#         self.consumer_lock = threading.Lock()
        
#         # At the begining the producer is allowed to add a new message, 
#         # but the consumer needs to wait until a message is present.
#         self.consumer_lock.acquire()

#     def get_message(self, name):
#         logging.debug("%s:about to acquire getlock", name)

#         # make the consumer wait until a message is ready.
#         self.consumer_lock.acquire()
#         logging.debug("%s:have getlock", name)


#         # It might seem tempting to get rid of message and just have the function 
#         # end with return self.message. But this can lead to race condition: 
#         # As soon as the consumer calls .producer_lock.release(), it can be swapped out, 
#         # and the producer can start running. That could happen before .release() returns! 
#         # This means that there is a slight possibility that when the function returns 
#         # self.message, that could actually be the next message generated, so you would 
#         # lose the first message. This is another example of a race condition.
#         message = copy.copy(self.message)
#         logging.debug("Message copied: %s. %s:about to release setlock", message, name)
        
#         # allow the producer to insert the next message into the pipeline
#         self.producer_lock.release()
#         logging.debug("%s:setlock released", name)
#         return message

#     def set_message(self, message, name):
#         logging.debug("%s:about to acquire setlock", name)
#         self.producer_lock.acquire()
#         logging.debug("%s:have setlock", name)
#         self.message = copy.copy(message)
#         logging.debug("%s:about to release getlock", name)
#         self.consumer_lock.release()
#         logging.debug("%s:getlock released", name)



# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#     logging.getLogger().setLevel(logging.DEBUG)

#     pipeline = Pipeline()
    
#     consumer = threading.Thread(target=consumer, args=(pipeline, ), daemon=True)
#     consumer.start()

#     producer = threading.Thread(target=producer, args=(pipeline, ), daemon=True)
#     producer.start()

#     consumer.join()
#     producer.join()

#     # # Alternative:
#     # with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#     #     executor.submit(producer, pipeline)
#     #     executor.submit(consumer, pipeline)





# ========================================================
# 
# https://stackoverflow.com/questions/16567958/when-and-how-to-use-pythons-rlock
#
# # ..... RLock vs. Lock ..... 
#
# # Rlock Useful when
# #  you want to have thread-safe access from outside the class and use the same methods from inside the class:

# class X:
#     def __init__(self):
#         self.a = 1
#         self.b = 2
#         self.lock = threading.RLock()

#     def changeA(self):
#         with self.lock:
#             self.a = self.a + 1

#     def changeB(self):
#         with self.lock:
#             self.b = self.b + self.a

#     def changeAandB(self):
#         # you can use chanceA and changeB thread-safe!
#         with self.lock:
#             self.changeA() # a usual lock would block at here
#             self.changeB()


# # for recursion more obvious:

# lock = threading.RLock()
# def a(...):
#      with lock:

#          a(...) # somewhere inside

# # other threads have to wait until the first call of a finishes = thread ownership.


# ==================================================
# 
# import threading
# 
# l = threading.Lock()
# print("before first acquire")
# l.acquire()
# print("before second acquire")
# l.acquire()     # Hangs here ... an acquired Lock cannot be acquired again (same thread)
# print("acquired lock twice")


# ==================================================
# 
# 
# import logging
# import threading
# import time
# import concurrent.futures


# class FakeDatabase:
#     def __init__(self):
#         self.value = 0
#         self._lock = threading.Lock()

#     def locked_update(self, name):
#         logging.info("Thread %s: starting update", name)
#         logging.debug("Thread %s about to lock", name)
#         with self._lock:
#             logging.debug("Thread %s has lock", name)
#             # read
#             local_copy = self.value
            
#             # modify
#             local_copy += 1
#             time.sleep(0.1)
            
#             # write
#             self.value = local_copy
#             logging.debug("Thread %s about to release lock", name)
#         logging.debug("Thread %s after release", name)
#         logging.info("Thread %s: finishing update", name)


# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")
#     logging.getLogger().setLevel(logging.DEBUG)

#     database = FakeDatabase()
#     logging.info("Testing update. Starting value is %d.", database.value)

#     with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#         for index in range(2):
#             executor.submit(database.locked_update, index)

#     logging.info("Testing update. Ending value is %d.", database.value)







# ============================================

# >>> def inc(x):
# ...    x += 1
# ...
# >>> import dis
# >>> dis.dis(inc)
#   2           0 LOAD_FAST                0 (x)
#               2 LOAD_CONST               1 (1)
#               4 INPLACE_ADD
#               6 STORE_FAST               0 (x)
#               8 LOAD_CONST               0 (None)
#              10 RETURN_VALUE


# Here x is local to inc(). So no race condition happens. But if 
# x was global, there would be a race condition. 

# In the example below, the time.sleep() makes sure that the OS 
# swaps threads. 


# ==============================================
#
# import logging
# import threading
# import time
# import concurrent.futures


# class FakeDatabase:
#     def __init__(self):
#         self.value = 0

#     def update(self, name):
#         logging.info("Thread %s: starting update", name)

#         # The local_copy is thread safe
#         # but the FakeDB.value that gets updated from it
#         # is shared between thread (without lock).
#         # So here the race condition happens: 
#         # The two threads have interleaving access to a 
#         # single shared object, overwriting each other’s results. 

#         # read the data from the DB
#         local_copy = self.value

#         # do something with it  
#         local_copy += 1   
#         time.sleep(0.1)
        
#         # write the result into DB
#         self.value = local_copy

#         logging.info("Thread %s: finishing update", name)


# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")

#     database = FakeDatabase()
#     logging.info("Testing update. Starting value is %d.", database.value)

#     with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#         for index in range(2):
#             executor.submit(database.update, index)

#     logging.info("Testing update. Ending value is %d.", database.value)




# When the thread starts running .update(), it has its own version 
# of all of the data local to the function. In the case of 
# .update(), this is local_copy. This is definitely a good thing. 
# Otherwise, two threads running the same function would always 
# confuse each other. 

# All variables that are scoped (or local) to a function are 
# thread-safe.

 # thread_pool.submit() has a signature that allows both 
 # positional and named arguments to be passed to the function 
 # running in the thread:
#        .submit(function, *args, **kwargs)

# Race conditions can occur when two or more threads access 
# a shared piece of data or resource.



# ==================================================
# 
# import logging
# import threading
# import time
# import concurrent.futures


# def thread_function(name):
#     logging.info("Thread %s: starting", name)
#     time.sleep(2)
#     logging.info("Thread %s: finishing", name)


# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")

#     with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
#         executor.map(thread_function, range(3))


# The end of the with block causes the ThreadPoolExecutor to do 
# a .join() on each of the threads in the pool. It is strongly 
# recommended that you use ThreadPoolExecutor as a context manager 
# when you can so that you never forget to .join() the threads.

# Note: Using a ThreadPoolExecutor can cause some confusing errors.
# For example, if you call a function that takes no parameters, 
# but you pass it parameters in .map(), the thread will throw an 
# exception.
# Unfortunately, ThreadPoolExecutor will hide that exception, 
# and (in the case above) the program terminates with no output. 
# This can be quite confusing to debug at first.


# =================================================
#
# import logging
# import threading
# import time

# def thread_function(name):
#     logging.info("Thread %s: starting", name)
#     time.sleep(2)
#     logging.info("Thread %s: finishing", name)

# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, level=logging.INFO,
#                         datefmt="%H:%M:%S")

#     threads = list()
#     for index in range(3):
#         logging.info("Main    : create and start thread %d.", index)
#         x = threading.Thread(target=thread_function, args=(index,))
#         threads.append(x)
#         x.start()

#     for index, thread in enumerate(threads):
#         logging.info("Main    : before joining thread %d.", index)
#         thread.join()
#         logging.info("Main    : thread %d done", index)



# =================================================
#
# import logging
# import threading
# import time


# def thread_function(name):
#     logging.info("Thread %s: starting", name)
#     time.sleep(2)
#     logging.info("Thread %s: finishing", name)


# if __name__ == "__main__":
#     format = "%(asctime)s: %(message)s"
#     logging.basicConfig(format=format, 
#                         level=logging.INFO, 
#                         datefmt="%H:%M:%S")
    
#     logging.info("Main     : before creating thread")
#     x = threading.Thread(target=thread_function, 
#                          args=(1, ), 
#                          daemon=True)
#     logging.info("Main     : before runing thread")
#     x.start()
#     logging.info("Main     : wait for thread to finish")
#     x.join()
#     logging.info("Main     : all done")
#
#
#
#
# ===============================================================
# 
# https://www.google.com/search?q=python+make+module+thread+safe&oq=python+make+module+thread+safe&aqs=chrome..69i57j69i64.6413j0j4&sourceid=chrome&ie=UTF-8
# # https://realpython.com/intro-to-python-threading/
# https://www.google.com/search?q=python+thread+local&oq=python+thread+local&aqs=chrome..69i57j0i457j0l5.5838j0j4&sourceid=chrome&ie=UTF-8
# https://www.bogotobogo.com/python/Multithread/python_multithreading_Thread_Local_Specific_Data.php
# http://www.laurentluce.com/posts/python-threads-synchronization-locks-rlocks-semaphores-conditions-events-and-queues/
# https://www.google.com/search?sxsrf=ALeKk00QmV6Kh7WtDd6IHC-ikjNHCJu-Ig%3A1607692291324&ei=A3DTX7q2E8LggwftkqHgBQ&q=python+modules+shared+between+threads&oq=python+modules+shared+between+threads&gs_lcp=CgZwc3ktYWIQAzIICCEQFhAdEB46BAgAEEc6CwgAEMkDEJECEIsDOggIABCRAhCLAzoFCAAQiwM6CAgAEMkDEJECOgUIABDJAzoCCAA6CQgAEMkDEBYQHjoGCAAQFhAeOggIABAWEAoQHjoICAAQCBANEB5Qk9kBWLWgAmCkpgJoBHACeACAAa8CiAHGM5IBCTIuMTkuMTMuMZgBAKABAaoBB2d3cy13aXrIAQi4AQLAAQE&sclient=psy-ab&ved=0ahUKEwj6w7q_gMbtAhVC8OAKHW1JCFwQ4dUDCA0&uact=5
# https://stackoverflow.com/questions/19790570/using-a-global-variable-with-a-thread
# https://stackoverflow.com/questions/50922923/python-multithreading-with-shared-variable
# https://stackoverflow.com/questions/17774768/python-creating-a-shared-variable-between-threads
# https://www.pythonforthelab.com/blog/handling-and-sharing-data-between-threads/
# https://stackoverflow.com/questions/8309902/are-python-instance-variables-thread-safe
#
