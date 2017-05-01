from .Servo import Servo


class Lock(Servo):
    """The lock"""
    def __init__(self):
        super().__init__()
        self.locked = False

    def lock(self):
        """Lock the lock"""
        self.set_position(180)
        self.locked = True

    def unlock(self):
        """Unlock the lock"""
        self.set_position(0)
        self.locked = False

    def toggle(self):
        """Toggle the lock based on state"""
        if self.locked:
            self.unlock()
        else:
            self.lock()
