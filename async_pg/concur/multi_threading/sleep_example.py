# From here: 
# https://www.youtube.com/watch?v=IEEhzQoKtQU



"""
1. Non-concurrent
--------------------
The first do_something() function is run and finishes, 
then the second do_something() function is run. 

Both take all together around 1+1=2 seconds. 
"""
# import time


# start = time.perf_counter()

# def do_something():
#     print("Sleep 1 second...")
#     time.sleep(1)
#     print("Done sleeping ...")


# do_something()
# do_something()

# finish = time.perf_counter()
# print(f"Finished in {round(finish - start, 2)} second(s).")


"""
2. Concurrent
--------------------
The first do_something() function is run and reaches waiting 
(e.g. sleeping, io operation, etc.). As soon as the first function 
is waiting, the second function starts running. 
This way they (seem) to run concurrently. (Note that in python, 
because of GIL only one thread can run at a time, so two threads 
cannot run in reality at the same time. It seems only that they 
run at the same time, because as the thread1 is waiting, thread2
executes) 

Both takes all together around 1 seconds. 
"""

# import threading
# import time


# start = time.perf_counter()

# def do_something():
#     print("Sleep 1 second...")
#     time.sleep(1)
#     print("Done sleeping ...")


# t1 = threading.Thread(target=do_something)
# t2 = threading.Thread(target=do_something)

# # we need to start the thread, otherwise nothing happens. 
# t1.start()
# t2.start()

# # Here the main thread halts (waits) until t1 and 
# # then t2 are completed, before moving on.
# t1.join()
# t2.join()

# finish = time.perf_counter()
# print(f"Finished in {round(finish - start, 2)} second(s).")


"""
3. Many concurrent tasks
---------------------------
The first do_something() function is run and reaches waiting 
(e.g. sleeping, io operation, etc.). As soon as the first function 
is waiting, the second function starts running. An so on ...

Even we run 10 tasks, it still takes around 1 second together. 
"""

# import threading
# import time

# start = time.perf_counter()

# def do_something():
#     print("Sleep 1 second...")
#     time.sleep(1)
#     print("Done sleeping ...")


# threads = []
# for _ in range(10):
#     t = threading.Thread(target=do_something)
#     t.start()
#     threads.append(t)

# for t in threads:
#     t.join()

# finish = time.perf_counter()
# print(f"Finished in {round(finish - start, 2)} second(s).")


"""
4. Passing variables to the function 
-------------------------------------
The first do_something() function is run and reaches waiting 
(e.g. sleeping, io operation, etc.). As soon as the first function 
is waiting, the second function starts running. An so on ...
This time we pass the sleeping time to the functions.

Even we run 10 tasks, it still takes around 1 second together. 
"""

# import threading
# import time

# start = time.perf_counter()

# def do_something(seconds):
#     print(f"Sleep {seconds} second(s)...")
#     time.sleep(seconds)
#     print("Done sleeping ...")


# threads = []
# for _ in range(10):
#     t = threading.Thread(target=do_something, args=[1.5])
#     t.start()
#     threads.append(t)

# for t in threads:
#     t.join()

# finish = time.perf_counter()
# print(f"Finished in {round(finish - start, 2)} second(s).")


"""
5. Thread Pool 
-----------------
Introduced in Python 3.2
Easier and more efficient that creating an managing many threads 
manually.
If we want to transit our code later to multi-processing, it will 
be easier. 

It is better to use the ThreadPoolExecuter with a context manager. 

"""

# import concurrent.futures
# import time

# start = time.perf_counter()

# def do_something(seconds):
#     print(f"Sleep {seconds} second(s)...")
#     time.sleep(seconds)
#     return "Returning value: Done sleeping ..."


# with concurrent.futures.ThreadPoolExecutor() as executer:
#     # If we want to execute the functions once at a time. 
#     # The .submit() method schedules a function to be executed
#     # and returns a future object. 
#     # The future object encapsulates the execution of our function, 
#     # and allows us to check in on it after is has been scheduled, 
#     # e.g. we can check if it is running, if it is done, and we can 
#     # grab the results. 
#     f1 = executer.submit(do_something, *(1.5, ))
#     f2 = executer.submit(do_something, *(1.5, ))
    
#     print(f1.result())
#     print(f2.result())


# finish = time.perf_counter()
# print(f"Finished in {round(finish - start, 2)} second(s).")


"""
5. Thread Pool 2 
-----------------
We can create a list of futures using ThreadPoolExecuter and 
work with them.
We can use the as_completed() method to get those that complete in 
the order they complete.  

"""

# import concurrent.futures
# import time

# start = time.perf_counter()

# def do_something(seconds):
#     print(f"Sleep {seconds} second(s)...")
#     time.sleep(seconds)
#     return f"Returning value: Done sleeping {seconds} second(s)... "


# with concurrent.futures.ThreadPoolExecutor() as executer:
#     # If we want to execute the function multiple times
#     secs = [5, 4, 3, 2, 1]
#     futures = [executer.submit(do_something, sec) for sec in secs]
    
#     # The as_completed() method gives us an iterator, that we can loop 
#     # over and yields the results of our threads as they are completed.
#     # This way for example we can work on the results in the order they
#     # completed. 
#     for f in concurrent.futures.as_completed(futures):
#         print(f.result())


# finish = time.perf_counter()
# print(f"Finished in {round(finish - start, 2)} second(s).")


"""
5. Thread Pool with map() function 
------------------------------------
The submit() method, submits each function once at a time. So, in order
to apply functions on elements of an list for example, we had to use
a loop or list comprehension. 

Instead we can use the map() method to run our function over a list 
of values. In contrast to submit() function, the map() function directly
returns the result. It also sends the results in the order the threads
starts. 

Note that if our function raises an exception, It won't actually raise 
the exception while running the thread. The exception is raise while 
we retrieve the result form the results iterator. So if we need to 
handle the exception, we should do it as we retrieve the result. 

Another point with the thread pool is it automatically joins all the 
threads, and lets them finish before continueing to main thread.

"""

import concurrent.futures
import time

start = time.perf_counter()

def do_something(seconds):
    print(f"Sleep {seconds} second(s)...")
    time.sleep(seconds)
    return f"Returning value: Done sleeping {seconds} second(s)... "


with concurrent.futures.ThreadPoolExecutor() as executer:
    # If we want to execute the function multiple times
    secs = [5, 4, 3, 2, 1]
    results = executer.map(do_something, secs)
    for result in results:
        print(result)

finish = time.perf_counter()
print(f"Finished in {round(finish - start, 2)} second(s).")

