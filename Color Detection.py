import cv2
from PIL import Image
import numpy as np


def get_limits(color):
    c = np.uint8([[color]])  # BGR values
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    hue = hsvC[0][0][0]  # Get the hue value

    # Handle red hue wrap-around
    if hue >= 165:  # Upper limit for divided red hue
        lower_Limit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upper_Limit = np.array([180, 255, 255], dtype=np.uint8)
    elif hue <= 15:  # Lower limit for divided red hue
        lower_Limit = np.array([0, 100, 100], dtype=np.uint8)
        upper_Limit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    else:
        lower_Limit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upper_Limit = np.array([hue + 10, 255, 255], dtype=np.uint8)

    return lower_Limit, upper_Limit


yellow = [0,0,255]  # Orange in BGR colorspace
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerLimit, upperLimit = get_limits(color=yellow)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    mask_ = Image.fromarray(mask)

    bbox = mask_.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox

        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()
