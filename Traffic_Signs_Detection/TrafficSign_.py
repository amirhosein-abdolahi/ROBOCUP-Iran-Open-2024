import os
import cv2

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load the Haar cascade classifiers for each traffic sign
cascade_files = {
    'stop': 'XML\\Stop.xml',
    'yield': 'XML\\yield.xml',
    'right': 'XML\\right.xml',
    'left': 'XML\\left.xml',
    
    # Add cascade files for other traffic signs here
}

# Load the pre-trained classifiers
classifiers = {name: cv2.CascadeClassifier(file) for name, file in cascade_files.items()}

# Webcam setup
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't capture frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect traffic signs using each classifier
    for sign_name, classifier in classifiers.items():
        signs = classifier.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in signs:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, sign_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    cv2.imshow('Traffic Sign Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'Q' to exit
        break

cap.release()
cv2.destroyAllWindows()
