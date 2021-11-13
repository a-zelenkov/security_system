import face_recognition
import cv2
import numpy as np
import json
import os
import threading
import time

# WARNING: чтобы работал tts, нужно установить festvox. 
# sudo apt-get install festvox-ru

DATABASE_FILE = 'db.json'
FONT = cv2.FONT_HERSHEY_DUPLEX
GREETINGS_INTERVAL = 10 #seconds

FACES = []
NAMES_RUSSIAN = []
NAMES = []
GREETINGS = []
REC_PROCESSES = []
SKIP_INDEXES = []

try:
    with open(DATABASE_FILE, 'r', encoding='utf-8') as read_file:
        persons = json.load(read_file)
except:
    persons = []

for person in persons:
    NAMES.append(person['name'])
    NAMES_RUSSIAN.append(person['name_russian'])
    FACES.append(person['face'])
    GREETINGS.append(False)
    REC_PROCESSES.append(0)

def greetings(index, name):
    os.system("echo 'Добро пожаловать, " + name + "' | festival --tts --language russian")
    time.sleep(GREETINGS_INTERVAL)
    GREETINGS[index] = False

video_capture = cv2.VideoCapture(0)
while True:
    ret, frame = video_capture.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(FACES, face_encoding)
        name = "Unknown"
        color = (0, 0, 255) #BGR

        face_distances = face_recognition.face_distance(FACES, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            color = (0, 255, 255) #BGR
            REC_PROCESSES[best_match_index] += 10
            name = NAMES[best_match_index] + '?'
            SKIP_INDEXES.append(best_match_index)
            if REC_PROCESSES[best_match_index] >= 100:
                REC_PROCESSES[best_match_index] = 100
                name = NAMES[best_match_index]
                color = (0, 255, 0) #BGR
                if not GREETINGS[best_match_index]:
                    thread = threading.Thread(target=greetings, args=(best_match_index,NAMES_RUSSIAN[best_match_index]))
                    thread.start()     
                    GREETINGS[best_match_index] = True
                    

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0,0,0), cv2.FILLED)
        cv2.line(frame, (left, bottom-36), (right, bottom-36), color, 3)

        #progress bar
        cv2.rectangle(frame, (left, top - 35), (right, top), color, 4)
        cv2.rectangle(frame, (left, top - 35), (int(left + ((right - left) / 100) * REC_PROCESSES[best_match_index]), top), color, cv2.FILLED)

        cv2.rectangle(frame, (left, top), (right, bottom), color, 4)
        cv2.putText(frame, name, (left + 6, bottom - 6), FONT, 1.0, (255, 255, 255), 1)
    
    for i in range(len(REC_PROCESSES)):
        if not i in SKIP_INDEXES:
            REC_PROCESSES[i] = 0

    SKIP_INDEXES = []

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
