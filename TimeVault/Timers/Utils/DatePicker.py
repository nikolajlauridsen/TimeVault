import RPi.GPIO as GPIO
import time

from .TimeHelp import convert_unix, convert_timestamp
from .Exceptions import NotInitializedError


class DatePicker:
    """Object for choosing a date and time, down to the minute"""
    def __init__(self, screen, buttons):
        self.screen = screen
        self.buttons = buttons

        # Time string eg: 24/12/2017 18:47
        self.time_format = "%d/%m/%Y %H:%M"
        self.date = None  # String variable to hold the date
        self.time = None  # String variable to hold the time
        # Unix unix
        self.unix = None

    def pick_date(self):
        """Prompt the user to pick a date"""
        # Initialize with the current date
        _time = time.time()
        day = int(convert_unix(_time, "%d"))
        month = int(convert_unix(_time, "%m"))
        year = int(convert_unix(_time, "%Y"))
        current_year = year

        # Main loop
        while True:
            date = "{:02}/{:02}/{:04}".format(day, month, year)
            # Update screen
            self.screen.lcd_display_string("Choose date".center(16), 1)
            self.screen.lcd_display_string(date.center(16), 2)

            if GPIO.event_detected(self.buttons["d_up"]):
                if day < 32:  # TODO: Usual actual max day of month
                    day += 1
                else:
                    day = 32

            if GPIO.event_detected(self.buttons["d_down"]):
                if day > 1:
                    day -= 1
                else:
                    day = 32  # TODO: Usual actual max day of month

            if GPIO.event_detected(self.buttons["hr_up"]):
                if month < 12:
                    month += 1
                else:
                    month = 1

            if GPIO.event_detected(self.buttons["hr_down"]):
                if month > 1:
                    month -= 1
                else:
                    month = 12

            if GPIO.event_detected(self.buttons["mn_up"]):
                year += 1

            if GPIO.event_detected(self.buttons["mn_down"]):
                if year > current_year:
                    year -= 1
                else:
                    year = current_year

            if GPIO.event_detected(self.buttons["start"]):
                self.date = date
                break

            if GPIO.event_detected(self.buttons["stop"]):
                # Selection has been canceled, reset date
                self.date = None
                break

            time.sleep(0.2)

    def pick_time(self):
        """Prompt the user to pick a time of day"""
        # Initialize with the current time
        _time = time.time()
        hr = int(convert_unix(_time, "%H"))
        mn = int(convert_unix(_time, "%M"))

        # Main loop
        while True:
            # Update stamp and screen
            stamp = "{:02}:{:02}".format(hr, mn)
            self.screen.lcd_display_string("Choose time".center(16), 1)
            self.screen.lcd_display_string(stamp.center(16), 2)

            if GPIO.event_detected(self.buttons["d_up"]):
                if hr < 23:
                    hr += 1
                else:
                    hr = 0

            if GPIO.event_detected(self.buttons["d_down"]):
                if hr > 0:
                    hr -= 1
                else:
                    hr = 23

            if GPIO.event_detected(self.buttons["hr_up"]):
                if mn < 59:
                    mn += 1
                else:
                    mn = 0

            if GPIO.event_detected(self.buttons["hr_down"]):
                if mn > 0:
                    mn -= 1
                else:
                    mn = 59

            if GPIO.event_detected(self.buttons["start"]):
                self.time = stamp
                break

            if GPIO.event_detected(self.buttons["stop"]):
                # Selection was canceled reset day
                self.time = None
                break

            time.sleep(0.2)

    def pick_datetime(self):
        """Prompt the user to select a datetime and sets unix"""
        self.pick_date()
        if self.date:
            self.pick_time()
        else:
            # User stopped prematurely, reset unix and step out of method
            self.unix = None
            return

        if self.date and self.time:
            stamp = self.date + " " + self.time
            self.unix = convert_timestamp(stamp, "%d/%m/%Y %H:%M")
        else:
            self.unix = None

    def get_unix(self):
        """Return the unix stamp created during pick_datetime"""
        if self.unix:
            return self.unix
        else:
            raise NotInitializedError("date_picker not properly initialized")
