
import sys
import subprocess
import threading
import signal
import time


_stop = False

def read_klv():
    # TODO: read the command from config and split it. 
    klvproc = subprocess.Popen(["ffmpeg", "-i", "udp://127.0.0.1:11111", 
                               "-map",  "0:1",  "-codec", "copy",  
                               "-f", "data",  "-"], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
    
    print("FFMPEG command called: ", klvproc.args)

    # If we need to get the stderr of ffmpeg as well, we should open 
    # another thread.
    with open("dummy.klv", "bw") as outfile:   
        while not _stop:
            data = klvproc.stdout.read(1024)
            outfile.write(data)
    
    klvproc.stdout.close()
    klvproc.terminate()  # same as writing q to stdin, return code 255
    klvproc.wait()
    print("Return code: ", klvproc.returncode) # 255, received_sigterm
    

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

