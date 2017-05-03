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
        if duty == 100:
            # My servo freaks out at 100, so minus it with one
            # This doesn't seem to change the final position either
            duty -= 1
        if duty == 0:
            # Same goes for 0
            duty += 1

        self.pwm.ChangeDutyCycle(duty)
