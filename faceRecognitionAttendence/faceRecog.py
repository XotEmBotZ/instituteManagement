import datetime
import cv2
import numpy as np
import face_recognition
import config

if config.ASK_VALUES_ON_STARTUP:
    serverUrl=input("Server URL:")
    sercerSecret=input("Server Secret")


video=cv2.VideoCapture(config.WEBCAM_INDEX)
absentStd=set()

while True:
    _,frame=video.read()

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()