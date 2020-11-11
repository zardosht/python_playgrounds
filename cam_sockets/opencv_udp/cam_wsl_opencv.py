from cv2 import cv2
import numpy as np


def main():
    cap = cv2.VideoCapture("udp://127.0.0.1:5000")
    if cap.isOpened():    
        while(True):
            ret, frame = cap.read()
            print("Received frame: ", frame.shape)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            cv2.imshow("Video Stream", gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    
    else:
        print("Could not open cv2.VideoCapture(\"UDP://127.0.0.1:5000\")")


if __name__ == "__main__":
    main()



# Run the following command to stream your built-in webcam to the 
# UDP address udp://127.0.0.1:5000
# FFMPEG must be installed. You may need to change the device name. 
# For finding out device names run: 
# C:\> ffmpeg -list_devices true -f dshow -i dummy
#
# To stream run: 
#
# C:\> ffmpeg -f dshow -i video="Integrated Camera" -preset ultrafast 
#             -tune zerolatency -vcodec libx264 -r 10 -b:v 2014k 
#             -s 640x480 -ab 32k -ar 44100 -f mpegts -flush_packets 0 
#             udp://127.0.0.1:5000?pkt_size=1316
#
# In one line, and with an alternative to make FFMPEG start streaming 
# faster (has no effect though)
# C:\> ffmpeg -f dshow -i video="Integrated Webcam" -preset ultrafast -tune zerolatency -vcodec libx264 -r 30 -b:v 2014k -s 640x480 -ab 32k -ar 44100 -f mpegts -flush_packets 0 udp://127.0.0.1:5000?pkt_size=1316
# C:\>  ffmpeg -f dshow -i video="Integrated Webcam" -preset ultrafast -tune zerolatency -vcodec libx264 -r 30 -b:v 2014k -s 640x480 -ab 32k -ar 44100 -f mpegts -flush_packets 0 -fflags nobuffer udp://127.0.0.1:5000?pkt_size=1316