import cv2

cap0 = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(2)

while True:
    ret0, frame0 = cap0.read()
    ret1, frame1 = cap1.read()
    
    if ret0 and ret1:
        cv2.imshow('Cam1', frame0)
        cv2.imshow('Cam2', frame1)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap0.release()
cap1.release()
cv2.destroyAllWindows()