"""
To get the proper window size and position, fix windows in the pos and then run this command on terminal:
$ xwininfo
"""

import cv2
from threading import Thread

from mq import MQ

LOGITEC_SOURCE = 0
GOPRO_VIDEO_SOURCE = "udp://@:8554?overrun_nonfatal=1&fifo_size=50000000"
FLIR_VIDEO_SOURCE = "/dev/video3"
ZOOM_RATIO = 50
WIN_NAME = 'GoPro'
WIN_WIDTH = 1055
WIN_HEIGHT = 702
WIN_X = 311
WIN_Y = 34


class ThreadedCamera(object):
    def __init__(self, source=0):

        self.capture = cv2.VideoCapture(source)

        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

        self.status = False
        self.frame = None

    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

    def grab_frame(self):
        if self.status:
            return self.frame
        return None


streamer = ThreadedCamera(LOGITEC_SOURCE)
cv2.namedWindow(WIN_NAME, cv2.WINDOW_NORMAL)
cv2.resizeWindow(WIN_NAME, WIN_WIDTH, WIN_HEIGHT)
cv2.moveWindow(WIN_NAME, WIN_X, WIN_Y)

# initialize sensors
# TODO: define sensors here
# mq_2 = MQ(4, "Methane, Butane, LPG, Smoke")
# mq_7 = MQ(13, "Carbon Monoxide")
# sensor_objs = [mq_2, mq_7]
sensor_objs = []

while True:
    frame = streamer.grab_frame()

    if frame is None:
        continue

    # get the webcam size
    height, width, channels = frame.shape

    # prepare the crop
    centerX, centerY = int(height / 2), int(width / 2)
    radiusX, radiusY = int(ZOOM_RATIO * height / 100), int(ZOOM_RATIO * width / 100)

    minX, maxX = centerX - radiusX, centerX + radiusX
    minY, maxY = centerY - radiusY, centerY + radiusY

    cropped = frame[minX:maxX, minY:maxY]
    resized_cropped = cv2.resize(cropped, (width, height))

    for i, sensor in enumerate(sensor_objs):
        if sensor.is_detected():
            cv2.putText(
                img=resized_cropped,
                text=f"{sensor.display_title}: detected",
                org=(35, 35+(i*40)),
                fontFace=cv2.FONT_ITALIC,
                fontScale=0.75,
                color=(0, 0, 255),
                thickness=2
            )
        else:
            cv2.putText(
                img=resized_cropped,
                text=f"{sensor.display_title}: not detected",
                org=(35, 35+(i*40)),
                fontFace=cv2.FONT_ITALIC,
                fontScale=0.75,
                color=(0, 255, 0),
                thickness=2
            )

    cv2.imshow(WIN_NAME, resized_cropped)

    key = cv2.waitKey(1)

    if key == ord('q'):
        if ZOOM_RATIO < 50:
            ZOOM_RATIO += 0.5

    elif key == ord('w'):
        if ZOOM_RATIO > 1:
            ZOOM_RATIO -= 0.5

# When everything is done, release the capture
cv2.destroyAllWindows()
