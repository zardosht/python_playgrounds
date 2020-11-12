# From here: 
# https://www.youtube.com/watch?v=Mj-Pyg4gsPs
#

import asyncio
from itertools import islice

from aiohttp import ClientSession


# So, what we want to do is to make A LOT of request. 
# Like, too many to run them all in parallel, or too 
# many to queue them all up in memory. 


async def fetch(url):
    async with ClientSession() as s, s.get(url) as res:
        ret = await res.read()
        print(f"Received {len(ret)} bytes of response")
        return ret


# Note this is not a coroutine - it returns
# an iterator - but it crucially depends on
# work being done inside the coroutines it
# yields - those coroutines empty out the
# list of futures it holds, and it will not
# end until that list is empty.
async def limited_as_completed(coros, limit):
    """
     Takes a generator of awaitables.
     Limits the number of concurrent tasks 
    """

    # start the limited number of tasks
    futures = [
        asyncio.ensure_future(c)
        for c in islice(coros, 0, limit)
    ]
    
    # A coroutine that waits for one of the
    # futures to finish and then returns
    # its result.
    async def first_to_finish():

        # Wait forever - we could add a
        # timeout here instead.
        while True:
            # Give up control to the scheduler
            # - otherwise we will spin here
            # forever!
            await asyncio.sleep(0)

            # Return anything that has finished
            for f in futures:
                if f.done():
                    futures.remove(f)
                    try:
                        newf = next(coros)
                        futures.append(
                            asyncio.ensure_future(newf))
                    except StopIteration as e:
                        print(e)
                    return f.result()

    # Keep yielding a waiting coroutine
    # until all the futures have finished.
    while len(futures) > 0:
        yield first_to_finish()


async def print_when_done(tasks): 
    # pylint: disable=not-an-iterable
    for res in limited_as_completed(tasks, 1000):
        print(await res)

# coros is now a generator expression
coros = (
    fetch("http://example.com") for i in range(100_000_000)
)


## Obviously the below code would not work! because 
# 1. we cannot keep 100M objects in a list.
# 2. Although as_compoleted() would return an iterator, 
#    this code would launch 100M request, because, of the 
#    async with in fetch() 
# So we need something like the limited_as_completed()
#  
# async def print_when_done(tasks): 
#     for res in asyncio.as_completed(tasks):
#         print(await res)
#
# coros = [
#     fetch("http://example.com") for i in range(100_000_000)
# ]


loop = asyncio.get_event_loop()
loop.run_until_complete(print_when_done(coros))
loop.close()




# ======================================================

# async def mycoro(number):
#     print("Starting %d" % number)
#     await asyncio.sleep(1)
#     print("Finishing %d" % number)   # runs later
#     return str(number)


# # c = mycoro(100)
# # task = asyncio.ensure_future(c)

# # # or Python 3.7 above: 
# # task = asyncio.create_task(c)

# many = asyncio.gather(
#     mycoro(3),
#     mycoro(4),
#     mycoro(5)
# )


# loop = asyncio.get_event_loop()
# # print("Running 1 task c:")
# # loop.run_until_complete(task)
# print("Running many:")
# result = loop.run_until_complete(many)
# print(result)
# loop.close()

# ======================================================

# async def f2():
#     print("Start f2")
#     await asyncio.sleep(1)
#     print("Stop f2")


# async def f1():
#     print("Start f1")
#     await f2()
#     print("Stop f1")

# # # We can also give coroutines directly to event loop
# # # without creating a future from them.
# # task = asyncio.ensure_future(f1())

# loop = asyncio.get_event_loop()
# loop.run_until_complete(f1())
# loop.close()
