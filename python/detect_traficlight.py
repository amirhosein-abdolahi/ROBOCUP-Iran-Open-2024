import cv2
import numpy as np

# Capture video from the camera (you might need to adjust the camera index)
cap = cv2.VideoCapture(0)

# set the upper and lower HSV color values
lowerRed1 = np.array([0,100,100])
upperRed1 = np.array([10,255,255])
lowerRed2 = np.array([160,100,100])
upperRed2 = np.array([180,255,255])
lowerGreen = np.array([40,50,50])
upperGreen = np.array([90,255,255])
lowerYellow = np.array([15,150,150])
upperYellow = np.array([35,255,255])

while True:
    #Read frame from the video stream
    ret, frame = cap.read()
    if not ret:
        break

    # Get the size of frame
    size = frame.shape

    # Convert the frame to HSV format
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # craete the masks
    mask1 = cv2.inRange(hsvFrame, lowerRed1, upperRed1)
    mask2 = cv2.inRange(hsvFrame, lowerRed2, upperRed2)
    maskRed = cv2.add(mask1, mask2)
    maskGreen = cv2.inRange(hsvFrame, lowerGreen, upperGreen)
    maskYellow = cv2.inRange(hsvFrame, lowerYellow, upperYellow)

    # hough circle detect
    redCircle = cv2.HoughCircles(maskRed, cv2.HOUGH_GRADIENT, 1, 80,
                                 param1=50, param2=10, minRadius=0, maxRadius=30)
    greenCircle = cv2.HoughCircles(maskGreen, cv2.HOUGH_GRADIENT, 1, 60,
                                 param1=50, param2=10, minRadius=0, maxRadius=30)
    yellowCircle = cv2.HoughCircles(maskYellow, cv2.HOUGH_GRADIENT, 1, 30,
                                 param1=50, param2=5, minRadius=0, maxRadius=30)
    
    # detect trafic light
    r = 5
    bound = 0.4 # 40 percent

    # detect red light
    if redCircle is not None:
        
        # Round and change type 
        redCircle = np.uint16(np.around(redCircle))

        # Loop through the each circles
        for cir in redCircle[0, :]:

            # Check circle not fallout of frame
            # and not detect circles downe of the frame
            if cir[0] > size[1] or cir[1] > size[0] or cir[1] > size[0] * bound:
                continue
            
            # Check number of pixels inside the circle
            h, s = 0.0, 0.0 # h number of red pixels and s number of all pixels 
            for m in range(-r, r):
                for n in range(-r, r):
                    
                    # Check the pixels falling outside the circle
                    if (cir[1]+m) >= size[0] or (cir[0]+n) >= size[1]:
                        continue

                    h += maskRed[cir[1]+m, cir[0]+n]
                    s += 1
            
            if h / s > 50:
                cv2.circle(frame, (cir[0], cir[1]), cir[2] + 10, (0, 0, 255), 2)

    # detect green light
    if greenCircle is not None:
        
        # Round and change type 
        greenCircle = np.uint16(np.around(greenCircle))

        # Loop through the each circles
        for cir in greenCircle[0, :]:

            # Check circle not fallout of frame
            # and not detect circles downe of the frame
            if cir[0] > size[1] or cir[1] > size[0] or cir[1] > size[0] * bound:
                continue
            
            # Check number of pixels inside the circle
            h, s = 0.0, 0.0 # h number of red pixels and s number of all pixels 
            for m in range(-r, r):
                for n in range(-r, r):
                    
                    # Check the pixels falling outside the circle
                    if (cir[1]+m) >= size[0] or (cir[0]+n) >= size[1]:
                        continue

                    h += maskGreen[cir[1]+m, cir[0]+n]
                    s += 1
            
            if h / s > 100:
                cv2.circle(frame, (cir[0], cir[1]), cir[2] + 10, (0, 255, 0), 2)

    # detect yellow light
    if yellowCircle is not None:
        
        # Round and change type 
        yellowCircle = np.uint16(np.around(yellowCircle))

        # Loop through the each circles
        for cir in yellowCircle[0, :]:

            # Check circle not fallout of frame
            # and not detect circles downe of the frame
            if cir[0] > size[1] or cir[1] > size[0] or cir[1] > size[0] * bound:
                continue
            
            # Check number of pixels inside the circle
            h, s = 0.0, 0.0 # h number of red pixels and s number of all pixels 
            for m in range(-r, r):
                for n in range(-r, r):
                    
                    # Check the pixels falling outside the circle
                    if (cir[1]+m) >= size[0] or (cir[0]+n) >= size[1]:
                        continue

                    h += maskYellow[cir[1]+m, cir[0]+n]
                    s += 1
            
            if h / s > 50:
                cv2.circle(frame, (cir[0], cir[1]), cir[2] + 10, (0, 255, 255), 2)

    # show result
    cv2.imshow('detected results', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break