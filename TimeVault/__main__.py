import RPi.GPIO as GPIO
import time

from .Physical import LCD_driver as lcdDriver
from .Timers.timer import Timer

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

    # Run duration menu thus setting the duration
    timer_set = timer.start_duration_menu()
    if timer_set:
        timer.start()
        # Main timer loop
        while not timer.check_expired():
            screen.lcd_display_string("Waiting...", 1)
            screen.lcd_display_string(timer.get_remaining_string(), 2)

            if GPIO.event_detected(buttons["stop"]):
                print("Timer stopped")
                break
            time.sleep(0.2)
    else:
        print("Please choose a duration")

    # Let's clean up after our self, shall we?
    for button in buttons.values():
        GPIO.cleanup(button)

    screen.lcd_display_string("Program exited".center(16), 1)
    screen.lcd_display_string("Goodbye :)".center(16), 2)
