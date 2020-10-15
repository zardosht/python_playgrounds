from cv2 import cv2
import numpy as np


def main():
    cap = cv2.VideoCapture("udp://127.0.0.1:5000")
    if cap.isOpened():    
        while(True):
            ret, frame = cap.read()
            print("Received frame: ", frame.shape)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            cv2.imshow("Video Stram", gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    
    else:
        print("Could not open cv2.VideoCapture(\"UDP://127.0.0.1:5000\")")


if __name__ == "__main__":
    main()

