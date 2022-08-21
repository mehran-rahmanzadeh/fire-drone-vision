"""
To get the proper window size and position, fix windows in the pos and then run this command on terminal:
$ xwininfo
"""
import time

import cv2
from imutils.video import FPS
from imutils.video import WebcamVideoStream

GOPRO_VIDEO_SOURCE = "udp://@:8554"
FLIR_VIDEO_SOURCE = "/dev/video3"
ZOOM_RATIO = 50
WIN_NAME = 'GoPro'
WIN_WIDTH = 1055
WIN_HEIGHT = 702
WIN_X = 311
WIN_Y = 34


cap = WebcamVideoStream(src=GOPRO_VIDEO_SOURCE).start()
time.sleep(1.0)
fps = FPS().start()
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cv2.namedWindow(WIN_NAME, cv2.WINDOW_NORMAL)
cv2.resizeWindow(WIN_NAME, WIN_WIDTH, WIN_HEIGHT)
cv2.moveWindow(WIN_NAME, WIN_X, WIN_Y)

while True:
    frame = cap.read()

    # get the webcam size
    height, width, channels = frame.shape

    # prepare the crop
    centerX, centerY = int(height / 2), int(width / 2)
    radiusX, radiusY = int(ZOOM_RATIO * height / 100), int(ZOOM_RATIO * width / 100)

    minX, maxX = centerX - radiusX, centerX + radiusX
    minY, maxY = centerY - radiusY, centerY + radiusY

    cropped = frame[minX:maxX, minY:maxY]
    resized_cropped = cv2.resize(cropped, (width, height))

    cv2.imshow(WIN_NAME, resized_cropped)

    key = cv2.waitKey(1)
    fps.update()

    if key == ord('q'):
        if ZOOM_RATIO < 50:
            ZOOM_RATIO += 0.5

    elif key == ord('w'):
        if ZOOM_RATIO > 1:
            ZOOM_RATIO -= 0.5

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
