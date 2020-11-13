
import sys
import subprocess
import threading
import signal
import time


_stop = False

def read_klv():
        
    # klvproc = subprocess.Popen(["ffmpeg", "-i", "udp://127.0.0.1:11111", 
    #                            "-map",  "0:1",  "-codec", "copy",  "-f", "data",  "-"], 
    #                            stdout=subprocess.PIPE, 
    #                            stderr=subprocess.PIPE)
    
    # print("FFMPEG command called: ", klvproc.args)
    # while not _stop:
    #     with open("dummy.log", "w") as logfile: 
    #         line = klvproc.stderr.readline()
    #         err = line.decode().rstrip("\r\n")
    #         print("LOG: ", err)
    #         logfile.write(err)

    #     with open("dummy.klv", "bw") as outfile:   
    #         data = klvproc.stdout.read(1024)
    #         # print(data)
    #         outfile.write(data)

    # print("Return code: ", klvproc.returncode)
    
    a = 1
    print("Starting endless loop till _stop is set.")
    while not _stop:
        print("aaaa: ", a)
        a += 1
        time.sleep(1)

    print("_stop is set. Loop exited. ")



def stop():
    global _stop
    _stop = True
    print("Stopped. Thanks, bye!")


def start():
    """Entrypoint method."""
    print("Demo started...")

    t = threading.Thread(target=read_klv, daemon=True)
    t.start()
    
    print("Press ctrl+c to terminate.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop()
        t.join()


if __name__ == "__main__":
    start()

