import mediapipe
import face_recognition
import cv2
import CONFIG as config
import json
import requests


mp_face_detection = mediapipe.solutions.face_detection
faceDetection = mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.75)


video = cv2.VideoCapture(config.WEBCAM_INDEX)
if config.WEBCAM_CHANGE_RESOLUTION:
    video.set(cv2.CAP_PROP_FRAME_WIDTH,config.WEBCAM_WIDTH)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT,config.WEBCAM_HEIGHT)
frameWidth = video.get(cv2.CAP_PROP_FRAME_WIDTH)
frameHeight = video.get(cv2.CAP_PROP_FRAME_HEIGHT)


def main():
    encoding = None
    isStored = False

    while True:
        _, frame = video.read()
        rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        fcFaceLoc = []
        faceLoc = faceDetection.process(rgbFrame)
        if faceLoc.detections:
            for face in faceLoc.detections:
                faceBoundingBox = face.location_data.relative_bounding_box
                x1 = int(faceBoundingBox.xmin*frameWidth)
                y1 = int(faceBoundingBox.ymin*frameHeight)
                x2 = int(x1+faceBoundingBox.width*frameWidth)
                y2 = int(y1+faceBoundingBox.height*frameHeight)
                frame = cv2.circle(frame, (x1, y1), 5, (255, 255, 255), 3)
                frame = cv2.circle(frame, (x2, y2), 5, (255, 255, 255), 3)
                frame = cv2.rectangle(
                    frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                fcFaceLoc.append([y1, x2, y1, x1])
                break
        if isStored:
            frame = cv2.putText(frame, "Stored Face Cascade", (50, 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        frame = cv2.putText(frame, "hold q for quite & hold s for saving face data!", (10, int(
            frameHeight-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.imshow('Video', frame)
        waitKey=cv2.waitKey(1) & 0xFF
        if waitKey== ord('q'):
            break
        elif waitKey == ord('s'):
            faceEncoding = face_recognition.face_encodings(frame, fcFaceLoc)[0]
            encoding = faceEncoding
            isStored = True

    cv2.destroyAllWindows()

    if not isStored:
        return
    adminNo = int(input("Enter Admin Number of student:-"))
    finalize = input("Do you want to update it? write y/Y for yes! :-")
    if finalize == "Y" or finalize == "y":
        print("Updating.....")
        data = {
            "adminNo": adminNo,
            "faceCascade": list(encoding)
        }
        data = json.dumps(data)
        print("Status Code:-",requests.post(config.SERVER_URL, data=data).status_code)
    else:
        print("Skipping Update...")

while True:
    main()
    restart = input("Would You like to stop the programe? y/Y for yes :-")
    if restart == "Y" or restart == "y":
        break

video.release()