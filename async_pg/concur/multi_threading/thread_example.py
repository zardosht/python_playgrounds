

https://www.pythonforthelab.com/blog/handling-and-sharing-data-between-threads/
https://stackoverflow.com/questions/17774768/python-creating-a-shared-variable-between-threads
https://stackoverflow.com/questions/50922923/python-multithreading-with-shared-variable
https://stackoverflow.com/questions/19790570/using-a-global-variable-with-a-thread
https://www.google.com/search?sxsrf=ALeKk00QmV6Kh7WtDd6IHC-ikjNHCJu-Ig%3A1607692291324&ei=A3DTX7q2E8LggwftkqHgBQ&q=python+modules+shared+between+threads&oq=python+modules+shared+between+threads&gs_lcp=CgZwc3ktYWIQAzIICCEQFhAdEB46BAgAEEc6CwgAEMkDEJECEIsDOggIABCRAhCLAzoFCAAQiwM6CAgAEMkDEJECOgUIABDJAzoCCAA6CQgAEMkDEBYQHjoGCAAQFhAeOggIABAWEAoQHjoICAAQCBANEB5Qk9kBWLWgAmCkpgJoBHACeACAAa8CiAHGM5IBCTIuMTkuMTMuMZgBAKABAaoBB2d3cy13aXrIAQi4AQLAAQE&sclient=psy-ab&ved=0ahUKEwj6w7q_gMbtAhVC8OAKHW1JCFwQ4dUDCA0&uact=5
https://www.bogotobogo.com/python/Multithread/python_multithreading_Thread_Local_Specific_Data.php
https://www.google.com/search?q=python+thread+local&oq=python+thread+local&aqs=chrome..69i57j0i457j0l5.5838j0j4&sourceid=chrome&ie=UTF-8
https://realpython.com/intro-to-python-threading/
https://www.google.com/search?q=python+make+module+thread+safe&oq=python+make+module+thread+safe&aqs=chrome..69i57j69i64.6413j0j4&sourceid=chrome&ie=UTF-8




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
