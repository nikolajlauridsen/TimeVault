import RPi.GPIO as GPIO
import time

from TimeVault.Timers.timer import Timer


class DurationMenu:
    """Menu for locking the vault for a specified duration"""
    def __init__(self, screen, buttons, lock):
        self.screen = screen
        self.buttons = buttons
        self.lock = lock
        self.timer = Timer(self.screen, self.buttons)

    def __repr__(self):
        return """Duration Mode"""

    def run(self):
        timer_set = self.timer.start_duration_menu()
        if timer_set:
            self.timer.start()
            print("Locking and starting timer")
            self.lock.lock()
            # Wait for the timer
            self.screen.lcd_clear()
            while not self.timer.expired():
                self.screen.lcd_display_string("Waiting...", 1)
                self.screen.lcd_display_string(self.timer.get_remaining_string(), 2)

                if GPIO.event_detected(self.buttons["stop"]):
                    print("Timer stopped")
                    break

                time.sleep(0.2)

            print("Timer finished, unlocking")
            self.lock.unlock()
