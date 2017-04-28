import RPi.GPIO as GPIO
import time

from .Physical import LCD_driver as lcdDriver
from .Menus.DurationMenu import DurationMenu

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
    menu = [DurationMenu(screen, buttons)]
    # Cursor for the menu
    cursor = 0

    # Main loop
    while True:
        screen.lcd_display_string("Choose mode".center(16), 1)
        screen.lcd_display_string(str(menu[cursor]).center(16), 2)

        if GPIO.event_detected(buttons['d_down']):
            if cursor > 0:
                cursor -= 1
            else:
                cursor = len(menu) - 1

        elif GPIO.event_detected(buttons['hr_down']):
            if cursor < len(menu) - 1:
                cursor += 1
            else:
                cursor = 0

        elif GPIO.event_detected(buttons['start']):
            menu[cursor].run()

        elif GPIO.event_detected(buttons['stop']):
            break

        time.sleep(0.2)

    # Let's clean up after our self, shall we?
    for button in buttons.values():
        GPIO.cleanup(button)

    screen.lcd_display_string("Program exited".center(16), 1)
    screen.lcd_display_string("Goodbye :)".center(16), 2)
