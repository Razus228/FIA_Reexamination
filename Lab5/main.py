import threading
import cv2
from deepface import DeepFace

# Initialize camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Initialize counter
counter = 0
face_match = False
reference_img = cv2.imread("reference.jpg")

# Function to check face match
def check_face(frame):
    global face_match
    try:
        # Verify face using DeepFace (reduce frequency of checks)
        if DeepFace.verify(frame, reference_img.copy())['verified']:
            face_match = True
        else:
            face_match = False
    except ValueError:
        face_match = False

# Main loop
while True:
    ret, frame = cap.read()
    
    if ret:
        if counter % 100 == 0:  # Check every 500 frames
            # Run face detection in a separate thread
            threading.Thread(target=check_face, args=(frame.copy(),)).start()
        
        if face_match:
            cv2.putText(frame, "MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "NO MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        
        # Display frame
        cv2.imshow("video", frame)

        counter += 1

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
