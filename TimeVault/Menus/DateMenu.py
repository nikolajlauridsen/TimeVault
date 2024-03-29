import RPi.GPIO as GPIO
import time

# I've been coding too much java :(
from TimeVault.Timers.waiter import Waiter
from TimeVault.Timers.Utils.DatePicker import DatePicker
from TimeVault.Timers.Utils.Exceptions import NotInitializedError


class DateMenu:
    """Menu for locking the vault untill as specified time and date"""
    def __init__(self, screen, buttons, lock):
        self.screen = screen
        self.buttons = buttons
        self.lock = lock
        self.date_picker = DatePicker(self.screen, self.buttons)
        self.waiter = Waiter()

    def __repr__(self):
        return """Date Mode"""

    def run(self):
        self.date_picker.pick_datetime()
        try:
            self.waiter.set_end_time(self.date_picker.get_unix())
        except NotInitializedError:
            return  # TODO: User canceled the datetime selection, do something clever

        print("Locking box")
        self.lock.lock()
        self.screen.lcd_clear()
        while not self.waiter.expired():
            self.screen.lcd_display_string("Locked".center(16), 1)
            self.screen.lcd_display_string(self.waiter.get_remaining_stamp(), 2)

            if GPIO.event_detected(self.buttons["stop"]):
                print("Box manually opened")
                break

            time.sleep(0.2)

        print("We've arrived at the date and time! Unlocking box")
        self.lock.unlock()

