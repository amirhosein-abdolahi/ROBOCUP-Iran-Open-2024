import cv2

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    
    copy_frame = frame.copy()
    
    gray = cv2.cvtColor(copy_frame, cv2.COLOR_BGR2GRAY)
    
    bilateral = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)
    
    cany = cv2.Canny(bilateral, 50, 150)
    
    cv2.imshow("main", frame)
    cv2.imshow("bilateral", bilateral)
    cv2.imshow("cany", cany)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break