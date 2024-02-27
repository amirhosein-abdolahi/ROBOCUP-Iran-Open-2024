# Import libraries
import array
import cv2
import numpy as np

# Function for creating a region of interest (ROI)
def region_of_interest(frame, vertices):
    
    # Get size of frame
    height, width = frame.shape
    
    # Change type of vertices to array
    array_vertices = [np.array(vertices, np.int32)]
    
    # Create black frame
    mask = np.zeros_like(frame)
    
    # Draw a white region on black frame
    cv2.fillPoly(mask, array_vertices, 255)
    
    # Create roi
    roi = cv2.bitwise_and(frame, mask)
    
    return roi