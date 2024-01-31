import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # threshold on white/gray sidewalk stripes
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    # lower = (100,130,130)
    # upper = (180,200,200)
    # thresh = cv2.inRange(frame, lower, upper)
    # :D
    cv2.imshow('thresh', thresh)


    # apply morphology close to fill interior regions in mask
    kernel = np.ones((5, 5), np.uint8)
    morph = cv2.dilate(thresh, kernel)
    # morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    # :D
    cv2.imshow('morph1', morph)

    # kernel = np.ones((5, 5), np.uint8)
    # morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel)
    # # :D
    # cv2.imshow('morph2', morph)

    # get contours
    cntrs = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntrs = cntrs[0] if len(cntrs) == 2 else cntrs[1]

    # filter on area
    contours = frame.copy()
    good_contours = []
    for c in cntrs:
        area = cv2.contourArea(c)
        if area > 200:
            cv2.drawContours(contours, [c], -1, (0,0,255), 1)
            good_contours.append(c)
    # :D
    cv2.imshow('contours', contours)

    # combine good contours
    contours_combined = np.vstack(good_contours)

    # :D
    contours_combin= frame.copy()
    cv2.drawContours(contours_combin, contours_combined, -1, (255,0,0), 1)
    cv2.imshow('contours_combin', contours_combin)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break







# # get convex hull
# result = img.copy()
# hull = cv2.convexHull(contours_combined)
# cv2.polylines(result, [hull], True, (0,0,255), 2)

# # write result to disk
# cv2.imwrite("walkway_thresh.jpg", thresh)
# cv2.imwrite("walkway_morph.jpg", morph)
# cv2.imwrite("walkway_contours.jpg", contours)
# cv2.imwrite("walkway_result.jpg", result)

# # display it
# cv2.imshow("THRESH", thresh)
# cv2.imshow("MORPH", morph)
# cv2.imshow("CONTOURS", contours)
# cv2.imshow("RESULT", result)
# cv2.waitKey(0)