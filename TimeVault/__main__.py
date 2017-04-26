import time

import RPi.GPIO as GPIO

from .Physical import LCD_driver as lcdDriver
from .Timer.timer import Timer


def seconds_to_timestamp(seconds):
    """Convert seconds into a neatly formatted string.
    Format: DD:HH:MM
    Returns: Timestamp string."""
    days = seconds // (3600*24)
    hrs = (seconds % (3600*24)) // 3600
    mins = (seconds % 3600) // 60
    return "{:02}:{:02}:{:02}".format(int(days), int(hrs), int(mins))


buttons = {"start":   6,
           "stop":    5,
           "d_up":    24,
           "d_down":  23,
           "hr_up":   27,
           "hr_down": 25,
           "mn_up":   22,
           "mn_down": 17}

if __name__ == "__main__":
    # Set up channels
    GPIO.setmode(GPIO.BCM)
    # Buttons
    for button in buttons.values():
        # Setup input
        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # And event detection
        GPIO.add_event_detect(button, GPIO.RISING, bouncetime=300)

    # Initialize objects
    screen = lcdDriver.lcd()
    timer = Timer(screen, buttons)

    duration = 0
    # Main loop
    timer.start_duration_menu()

    print(timer.get_remaining_string())

    # Let's clean up after our self, shall we?
    for button in buttons.values():
        GPIO.cleanup(button)

    screen.lcd_display_string("Program exited".center(16))
    screen.lcd_display_string("Goodbye :)".center(16))
