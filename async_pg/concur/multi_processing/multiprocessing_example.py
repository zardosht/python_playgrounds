# From here: 
# https://www.youtube.com/watch?v=fKl2JW_qrso



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
2. Multi-processing
----------------------
Running tasks really at the same time on different CPUs (cores).


"""
# import multiprocessing
# import time


# start = time.perf_counter()

# def do_something():
#     print("Sleep 1 second...")
#     time.sleep(1)
#     print("Done sleeping ...")


# p1 = multiprocessing.Process(target=do_something)
# p2 = multiprocessing.Process(target=do_something)

# p1.start()
# p2.start()

# p1.join()
# p2.join()

# finish = time.perf_counter()
# print(f"Finished in {round(finish - start, 2)} second(s).")

## If we do not join() the processes, the output will be like this: 
##
## Finished in 0.02 second(s).
## Sleep 1 second...
## Sleep 1 second...
## Done sleeping ...
## Done sleeping ...
##
## The main thread finishes even before the processes are started. 

"""
3. Multiple executions of the task
-------------------------------------

"""

# import multiprocessing
# import time


# start = time.perf_counter()

# def do_something():
#     print("Sleep 1 second...")
#     time.sleep(1)
#     print("Done sleeping ...")


# processes = []
# for _ in range(10):
#     p = multiprocessing.Process(target=do_something)
#     p.start()
#     processes.append(p)

# for p in processes:
#     p.join()

# finish = time.perf_counter()
# print(f"Finished in {round(finish - start, 2)} second(s).")

"""
4. Passing arguments to the function (task)
--------------------------------------------

Notice that the arguments "must be serializable using Pickle". 
Remember it is inter-process communication. They are completely 
independent processes running in their own memory space. 

"""

# import multiprocessing
# import time


# start = time.perf_counter()

# def do_something(seconds):
#     print(f"Sleep {seconds} second...")
#     time.sleep(seconds)
#     print(f"Done sleeping ...{seconds}")


# processes = []
# for _ in range(10):
#     p = multiprocessing.Process(target=do_something, args=(1.5, ))
#     p.start()
#     processes.append(p)

# for p in processes:
#     p.join()

# finish = time.perf_counter()
# print(f"Finished in {round(finish - start, 2)} second(s).")

"""
5. Process Pool Executer
--------------------------

"""

# import concurrent.futures
# import time


# start = time.perf_counter()

# def do_something(seconds):
#     print(f"Sleep {seconds} second...")
#     time.sleep(seconds)
#     return f"Done sleeping ...{seconds}"


# with concurrent.futures.ProcessPoolExecutor() as executer:
#     # like multithreading, the submit() function schedules the function
#     # to be executed and returns a future object. 
#     futures = [executer.submit(do_something, 1.5) for _ in range(10)]
#     for f in futures:
#         print(f.result())

# # The ProcessPoolExecuter automatically joins the processes. 

# finish = time.perf_counter()
# print(f"Finished in {round(finish - start, 2)} second(s).")


"""
6. concurrent.futures.as_completed() 
--------------------------------------

Work on the futures in the order as they are completed. 

Result: 

Sleep 5 second...
Sleep 4 second...
Sleep 3 second...
Sleep 2 second...
Sleep 1 second...
Done sleeping ...1
Done sleeping ...2
Done sleeping ...3
Done sleeping ...4
Done sleeping ...5
Finished in 5.24 second(s).

"""
# import concurrent.futures
# import time


# start = time.perf_counter()

# def do_something(seconds):
#     print(f"Sleep {seconds} second...")
#     time.sleep(seconds)
#     return f"Done sleeping ...{seconds}"


# with concurrent.futures.ProcessPoolExecutor() as executer:
#     # like multithreading, the submit() function schedules the function
#     # to be executed and returns a future object. 
#     secs = [5, 4, 3, 2, 1]
#     futures = [executer.submit(do_something, sec) for sec in secs]
#     for f in concurrent.futures.as_completed(futures):
#         print(f.result())

# # The ProcessPoolExecuter automatically joins the processes. 

# finish = time.perf_counter()
# print(f"Finished in {round(finish - start, 2)} second(s).")


"""
7. ProcessPoolExecuter.map() 
------------------------------
map() returns the results in the same order as inputs. 

Result: 

Sleep 5 second...
Sleep 4 second...
Sleep 3 second...
Sleep 2 second...
Sleep 1 second...
Done sleeping ...5
Done sleeping ...4
Done sleeping ...3
Done sleeping ...2
Done sleeping ...1
Finished in 5.24 second(s).

"""

# import concurrent.futures
# import time


# start = time.perf_counter()

# def do_something(seconds):
#     print(f"Sleep {seconds} second...")
#     time.sleep(seconds)
#     return f"Done sleeping ...{seconds}"


# with concurrent.futures.ProcessPoolExecutor() as executer:
#     # like multithreading, the submit() function schedules the function
#     # to be executed and returns a future object. 
#     secs = [5, 4, 3, 2, 1]
#     results = executer.map(do_something, secs)
#     for result in results:
#         print(result)

# # The ProcessPoolExecuter automatically joins the processes. 

# finish = time.perf_counter()
# print(f"Finished in {round(finish - start, 2)} second(s).")

