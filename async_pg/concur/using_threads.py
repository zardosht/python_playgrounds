import concurrent.futures
import threading
import time

import requests


# Note: requests.Session() is not thread-safe. 

# thread local storage. Threading.local() creates an object that look 
# like a global but is specific to each individual thread.
thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url):
    session = get_session()
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")


def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_site, sites)


def concurrent_using_threads():
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")


def main():
    concurrent_using_threads()


if __name__ == "__main__":
    main()


# Result: notice how the downloads are unordered :)
#  
# Read 277 from http://olympus.realpython.org/dice
# Read 277 from http://olympus.realpython.org/dice
# Read 10394 from https://www.jython.org
# ...
# ...
# Read 10394 from https://www.jython.org
# Read 277 from http://olympus.realpython.org/dice
# Read 10394 from https://www.jython.org
# Read 277 from http://olympus.realpython.org/dice
# Read 10394 from https://www.jython.org
# Read 10394 from https://www.jython.org

# Downloaded 160 in 3.7479004859924316 seconds
