import cv2
import face_recognition

def getFaceFromWebCam():
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("Photo - 'space'")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("ошибка захвата камеры")
            break
        cv2.imshow("Photo - 'space'", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            break
        elif k%256 == 32:
            face_encoding = face_recognition.face_encodings(frame)[0].tolist()
            break

    cam.release()
    cv2.destroyAllWindows()
    return face_encoding

def getFaceFromImg(file):
    return face_recognition.face_encodings(face_recognition.load_image_file(file))[0].tolist()