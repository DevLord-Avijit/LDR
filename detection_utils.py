import cv2
import numpy as np

def detect_laser_dot(frame, lower, upper):
    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # First red range
    mask1 = cv2.inRange(hsv, lower, upper)

    # Second red range for hue wrap-around
    lower_red2 = (170, 120, 120)
    upper_red2 = (180, 255, 255)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # Combine both masks
    mask = cv2.bitwise_or(mask1, mask2)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Get largest red spot
        c = max(contours, key=cv2.contourArea)
        ((x, y), r) = cv2.minEnclosingCircle(c)
        if r > 1:
            # Return tuple + mask (this keeps the unpacking logic valid)
            return (int(x), int(y), int(r)), mask

    # No detection → return None + mask
    return None, mask
