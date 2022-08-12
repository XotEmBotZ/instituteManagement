import cv2
import numpy as np
import face_recognition
import config
import json
import requests

if config.ASK_VALUES_ON_STARTUP:
    serverUrl=input("Server URL:")
    sercerSecret=input("Server Secret")

cascades=requests.get(config.SERVER_URL).json()
stdAdminNo=[]
stdKnownFaceCascade=[]
for a in cascades["cascade"]:
    stdAdminNo.append(a["student"])
    stdKnownFaceCascade.append(a["studentCascade"])
presentStd=set()


video=cv2.VideoCapture(config.WEBCAM_INDEX)

while True:
    names=[]
    _,frame=video.read()
    rgbFrame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    faceLocations=face_recognition.face_locations(rgbFrame)
    faceEncodings=face_recognition.face_encodings(rgbFrame,faceLocations)
    for faceEncoding in faceEncodings:
        matches = face_recognition.compare_faces(stdKnownFaceCascade, faceEncoding)
        name = 0
        face_distances = face_recognition.face_distance(stdKnownFaceCascade, faceEncoding)
        best_match_index = np.argmin(face_distances)
        print(matches[best_match_index])
        if matches[best_match_index]:
            name = stdAdminNo[best_match_index]
            names.append(name)
        else:
            names.append("NaN")
    for index,(y1,x1,y2,x2) in enumerate(faceLocations):
        frame=cv2.rectangle(frame,(x1,y1),(x2,y2),(255,255,255),3)
        frame=cv2.putText(frame,str(names[index]),(x2,y2),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
    presentStd.update(names)

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

presentStd.remove("NaN")
for std in presentStd:
    stdAdminNo.remove(std)
absentStd=stdAdminNo

video.release()
cv2.destroyAllWindows()