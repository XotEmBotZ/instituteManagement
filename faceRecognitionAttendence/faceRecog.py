import face_recognition
import cv2
import time
import mediapipe
import config
import json
import requests

if config.ASK_VALUES_ON_STARTUP:
    serverUrl=input("Server URL:")
    sercerSecret=input("Server Secret")

cascades=requests.get(config.SERVER_URL_GET).json()

stdAdminNo=[]
stdKnownFaceCascade=[]

for a in cascades["cascade"]:
    stdAdminNo.append(a["student"])
    stdKnownFaceCascade.append(a["studentCascade"])

presentStd=set()

mp_face_detection=mediapipe.solutions.face_detection 
faceDetection=mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.75)


video=cv2.VideoCapture(config.WEBCAM_INDEX)
frameWidth=video.get(cv2.CAP_PROP_FRAME_WIDTH)
frameHeight=video.get(cv2.CAP_PROP_FRAME_HEIGHT)

while True:
    _,frame=video.read()
    rgbFrame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    fcFaceLoc=[]
    faceLoc=faceDetection.process(rgbFrame)
    if faceLoc.detections:
        for face in faceLoc.detections:
            faceBoundingBox=face.location_data.relative_bounding_box
            x1=int(faceBoundingBox.xmin*frameWidth)
            y1=int(faceBoundingBox.ymin*frameHeight)
            x2=int(x1+faceBoundingBox.width*frameWidth)
            y2=int(y1+faceBoundingBox.height*frameHeight)
            frame=cv2.circle(frame,(x1,y1),5,(255,255,255),3)
            frame=cv2.circle(frame,(x2,y2),5,(255,255,255),3)
            frame=cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),1)
            fcFaceLoc.append([y1,x2,y1,x1])
        faceEncoding=face_recognition.face_encodings(frame,fcFaceLoc)
        for faceEnc in faceEncoding:
            compareFace=face_recognition.compare_faces(stdKnownFaceCascade,faceEnc)
            faceDistance=face_recognition.face_distance(stdKnownFaceCascade,faceEnc)
            if compareFace[faceDistance.argmin()]:
                presentStd.update(stdAdminNo[faceDistance.argmin()])

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

presentStd.remove("NaN")
for std in presentStd:
    stdAdminNo.remove(std)
absentStd=stdAdminNo
data={
    "absentStudents":absentStd,
}
print(requests.post(config.SERVER_URL_POST,data=json.dumps(data)).status_code)

video.release()
cv2.destroyAllWindows()