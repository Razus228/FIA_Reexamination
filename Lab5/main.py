import threading

import cv2
from deepface import DeepFace

# Define camera object (numbers inside bracket mean which camera will be used)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Set proportions/dimensions
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Initialize counter
counter = 0

face_match = False

lock = threading.Lock()

# Load reference image
reference_img = cv2.imread("C:/Users/vergi/OneDrive/Desktop/FIA-Reexamination/Lab5/reference.jpg")

# Check if the reference image and current frame have the same face
def check_face(frame):
    global face_match
    try:
        if DeepFace.verify(frame, reference_img.copy())['verified']: # Pass a copy of the image to the function
            face_match = True
        else:
            face_match = False
    
    except ValueError:
        with lock:
          face_match = False


while True:
    ret, frame = cap.read()

    if ret:
        if counter % 1200 == 0:
            try:
                threading.Thread(target=check_face, args=(frame.copy(),)).start()
            except ValueError:
                pass
            counter += 1

            if face_match:
                cv2.putText(frame, "MATCH!", (20,450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            else:
                cv2.putText(frame, "NO MATCH!", (20,450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
    
            cv2.imshow("video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    
cv2.destroyAllWindows()

