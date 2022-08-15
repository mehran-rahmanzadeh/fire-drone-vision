"""
To get the proper window size and position, fix windows in the pos and then run this command on terminal:
$ xwininfo
"""

import cv2

FLIR_VIDEO_SOURCE = "/dev/video3"
WIN_NAME = 'Flir'
WIN_WIDTH = 311
WIN_HEIGHT = 702
WIN_X = 0
WIN_Y = 34

cap = cv2.VideoCapture(FLIR_VIDEO_SOURCE)
cv2.namedWindow(WIN_NAME, cv2.WINDOW_NORMAL)
cv2.resizeWindow(WIN_NAME, 311, 702)
cv2.moveWindow(WIN_NAME, 0, 34)

while True:
    _, frame = cap.read()

    cv2.imshow(WIN_NAME, frame)

    key = cv2.waitKey(1)

    if key == 27:
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
