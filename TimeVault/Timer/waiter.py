import time

from .Utils.TimeHelp import convert_unix


class Waiter:
    """A class for waiting until a certain date and time"""
    def __init__(self):
        self.endTime = 0

    def set_end_time(self, end):
        """Set the expiration time as a UNIX timestamp"""
        self.endTime = end

    def expired(self):
        """Check if the waiter has finished"""
        if time.time() >= self.endTime:
            return True
        else:
            return False

    def get_remaining(self):
        """Get remaining time till endTime in seconds"""
        remaining = self.endTime - time.time()
        if remaining > 0:
            return remaining
        else:
            return 0

    def get_remaining_stamp(self):
        """Get the remaining time as a timestamp"""
        return self.convert_seconds(self.get_remaining())

    def get_end_stamp(self):
        """Return the end time as a datetime stamp"""
        return convert_unix(self.endTime, "%d/%m/%Y %H:%M")

    @staticmethod
    def convert_seconds(seconds):
        """Convert seconds into a neatly formatted string
        format xxdays HH:MM:SS"""
        days = seconds // (3600 * 24)
        hrs = (seconds % (3600 * 24)) // 3600
        mins = (seconds % 3600) // 60
        s = (seconds % 3600) % 60
        return "{:02}days {:02}:{:02}:{:02}".format(int(days), int(hrs),
                                                    int(mins), int(s))
