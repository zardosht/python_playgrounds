# Taken from here:
# https://realpython.com/python-concurrency/

# Non-concurrent downloading of web pages: 

import requests
import time


def download_site(url, session):
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")


def download_all_sites(sites):
    with requests.Session() as session:
        for url in sites:
            download_site(url, session)


def non_concurrent():
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")


def main():
    non_concurrent()


if __name__ == "__main__":
    main()



# Result: 
# 
# Read 10394 from https://www.jython.org
# Read 277 from http://olympus.realpython.org/dice
# ...
# ...
# Read 10394 from https://www.jython.org
# Read 277 from http://olympus.realpython.org/dice
# 
# Downloaded 160 in 18.831740856170654 seconds

