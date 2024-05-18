# Import libraries
import array
import cv2
import numpy as np

# Function for creating a region of interest (ROI)
def region_of_interest(frame, draw, vertices):
    
    # Change type of vertices to array
    array_vertices = [np.array(vertices, np.int32)]
    
    # Create black frame
    mask = np.zeros_like(frame)
    
    # Draw a white region on black frame
    cv2.fillPoly(mask, array_vertices, 255)
    
    # Create ROI
    roi = cv2.bitwise_and(frame, mask)
    
    # Draw the ROI
    cv2.polylines(draw, array_vertices, True, (240, 130, 50), 3)
    
    return roi, draw
