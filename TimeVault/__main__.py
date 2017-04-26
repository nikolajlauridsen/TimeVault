import time

import RPi.GPIO as GPIO

from .Physical import LCD_driver as lcdDriver


def seconds_to_timestamp(seconds):
    """Convert seconds into a neatly formatted string.
    Format: HH:MM:SS
    Returns: Timestamp string."""
    # TODO: Convert to days/hrs/minutes
    hrs = seconds //3600
    mins = (seconds % 3600) // 60
    s = (seconds % 3600) % 60
    return "{:02}:{:02}:{:02}".format(int(hrs), int(mins), int(s))


buttons = {"d_up":    24,
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

    duration = 0
    # Main loop
    while True:
        screen.lcd_display_string("Choose time", 1)
        screen.lcd_display_string(seconds_to_timestamp(duration), 2)

        if GPIO.event_detected(buttons["d_up"]):
            # One hour is 3200 seconds, so a day is 3200*24
            duration += 3600*24

        if GPIO.event_detected(buttons["d_down"]):
            duration -= 3600*24

        if GPIO.event_detected(buttons["hr_up"]):
            duration += 3600

        if GPIO.event_detected(buttons["hr_down"]):
            duration -= 3600

        if GPIO.event_detected(buttons["mn_up"]):
            duration += 60

        if GPIO.event_detected(buttons["mn_down"]):
            duration -= 60

        time.sleep(0.2)
