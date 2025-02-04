import threading
import cv2
from deepface import DeepFace
import os

# Initialize camera
def initialize_camera():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    return cap

cap = initialize_camera()

# Initialize counter
counter = 0
face_match = False
person_name = "Unknown"

# Directory containing reference images
reference_images_folder = "C:/Users/vergi/OneDrive/Desktop/FIA-Reexamination/Lab5/Images"

# Load reference images and corresponding names
reference_images = []
names = []

# Load all images from the folder and associate them with names
for filename in os.listdir(reference_images_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(reference_images_folder, filename)
        reference_images.append(cv2.imread(image_path))
        names.append(os.path.splitext(filename)[0])  # Use filename (without extension) as the name

# Function to check face match
def check_face(frame):
    global face_match, person_name
    try:
        # Loop through all reference images and compare
        for i, ref_img in enumerate(reference_images):
            result = DeepFace.verify(frame, ref_img)
            if result['verified']:
                face_match = True
                person_name = names[i]  # Get the name of the matched person
                return  # Exit the function once a match is found
        # If no match is found, set face_match to False and person_name to Unknown
        face_match = False
        person_name = "Unknown"
    except ValueError:
        face_match = False
        person_name = "Unknown"

# Main loop
while True:
    ret, frame = cap.read()

    if ret:
        if counter % 500 == 0:  # Check every 500 frames
            # Run face detection in a separate thread
            threading.Thread(target=check_face, args=(frame.copy(),)).start()
        
        if face_match:
            cv2.putText(frame, f"MATCH: {person_name}", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "NO MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        
        # Display frame
        cv2.imshow("video", frame)

        counter += 1

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    
    if key == ord("k"):
        print("Resetting camera...")
        cap.release()  # Release the current camera
        cap = initialize_camera()  # Reinitialize the camera

cap.release()
cv2.destroyAllWindows()
