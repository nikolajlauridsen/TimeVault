import RPi.GPIO as GPIO

SERVO_PIN = 18


class Servo:
    """Control a servo"""
    def __init__(self):
        GPIO.setup(18, GPIO.OUT)
        self.pwm = GPIO.PWM(18, 100)
        self.pwm.start(0)

    def set_position(self, angle):
        """Set the position of the servo"""
        duty = float(100 * (angle / 180))
        self.pwm.ChangeDutyCycle(duty)
