import RPi.GPIO as GPIO
import time

from .countdown import CountDown


class Timer(CountDown):
    """A countdown timer"""
    def __init__(self, screen, buttons):
        super().__init__()
        self.screen = screen
        self.buttons = buttons

    def change_duration(self, change):
        if self.duration + change > 0:
            # +- = - so we can safely just do += change
            self.duration += change
        else:
            self.duration = 0

    def start_duration_menu(self):
        """Run the duration menu and sets the duration"""
        while True:
            self.screen.lcd_display_string("Choose time", 1)
            self.screen.lcd_display_string(
                self.seconds_to_timestamp(self.duration).center(16), 2)

            if GPIO.event_detected(self.buttons["d_up"]):
                # One hour is 3200 seconds, so a day is 3200*24
                self.change_duration(3600*24)

            if GPIO.event_detected(self.buttons["d_down"]):
                self.change_duration(-(3600*24))

            if GPIO.event_detected(self.buttons["hr_up"]):
                self.change_duration(3600)

            if GPIO.event_detected(self.buttons["hr_down"]):
                self.change_duration(-3600)

            if GPIO.event_detected(self.buttons["mn_up"]):
                self.change_duration(60)

            if GPIO.event_detected(self.buttons["mn_down"]):
                self.change_duration(-60)

            if GPIO.event_detected(self.buttons["stop"]):
                self.duration = 0
                return False

            if GPIO.event_detected(self.buttons["start"]):
                return True

            time.sleep(0.2)
