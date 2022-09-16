import RPi.GPIO as GPIO


class MQ:
    """MQ-x helper class
    it uses digital out of MQ-x sensor
    """
    def __init__(self, pin, display_title=""):
        self.pin = pin
        self.display_title = display_title
        super(MQ, self).__init__()

    def is_detected(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        return GPIO.input(self.pin)
