import time
import random
import datetime
import keyboard
from pyHM import mouse

class Engine:
    LOOP_MIN_DELAY = 1.0
    LOOP_MAX_DELAY = 3.0
    MOUSE_MIN_DELAY = 0.2
    MOUSE_MAX_DELAY = 0.5
    KEY_MIN_DELAY = 0.2
    KEY_MAX_DELAY = 0.8

    def __init__(self):
        pass

    @staticmethod
    def Sleep(seconds: float = 0.0) -> None:
        """Sleep for the specified number of seconds."""
        time.sleep(seconds)

    @staticmethod
    def LoopSleep() -> None:
        """Sleep for a randomized delay between loops."""
        total_delay = Engine.RandomFloat(Engine.LOOP_MIN_DELAY, Engine.LOOP_MAX_DELAY)
        Engine.Sleep(total_delay)

    @staticmethod
    def MouseWait(base_delay: float = 0.0) -> None:
        """Wait for a randomized delay based on the base_delay and configured random range."""
        total_delay = base_delay + Engine.RandomFloat(Engine.MOUSE_MIN_DELAY, Engine.MOUSE_MAX_DELAY)
        Engine.Sleep(total_delay)
    
    @staticmethod
    def KeyWait(base_delay: float = 0.0) -> None:
        """Wait for a randomized delay based on the base_delay and configured random range."""
        total_delay = base_delay + Engine.RandomFloat(Engine.KEY_MIN_DELAY, Engine.KEY_MAX_DELAY)
        Engine.Sleep(total_delay)

    @staticmethod
    def MouseClick(button: str = "left", x: int = None, y: int = None) -> None:
        """Perform a mouse click at the specified coordinates (or current position if None)."""
        if x is not None and y is not None:
            mouse.move(x, y)
        mouse.down(button=button)
        Engine.MouseWait(0)
        mouse.up(button=button)

    @staticmethod
    def MouseDrag(start_x: int = None, start_y: int = None, end_x: int = None, end_y: int = None, duration: float = 0.0) -> None:
        """Perform a mouse drag from (start_x, start_y) to (end_x, end_y) over the specified duration."""
        if start_x is not None and start_y is not None:
            mouse.move(start_x, start_y)
        mouse.down()
        Engine.MouseWait(0)
        if end_x is not None and end_y is not None:
            mouse.move(end_x, end_y, duration=duration)
        Engine.MouseWait(0)
        mouse.up()

    @staticmethod
    def KeyPress(key: str) -> None:
        """Press and release a keyboard key with a small randomized delay."""
        keyboard.press(key)
        Engine.KeyWait(0)
        keyboard.release(key)

    @staticmethod
    def RandomFloat(min: float = 0.0, max: float = 1.0) -> float:
        """Return a random float between min and max."""
        return random.uniform(min, max)
    
    @staticmethod
    def CurrentTimeStamp() -> float:
        """Return the current time as a timestamp."""
        return datetime.datetime.now().timestamp()
    
    @staticmethod
    def TimeSince(start: float = 0.0) -> float:
        """Return the time elapsed since start."""
        return Engine.CurrentTimeStamp() - start
    
    @staticmethod
    def DelayPassed(start: float = 0.0, delay: float = 0.0) -> bool:
        """Check if the specified delay has passed since start."""
        return start <= 0 or delay <= 0 or Engine.TimeSince(start) >= delay
    
    @staticmethod
    def Log(message: str, end: str = "\n") -> None:
        """Print a log message with a timestamp including nanosecond precision."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Format with milliseconds
        print(f"[{timestamp}] {message}", end=end)

    @staticmethod
    def CleanConsole() -> None:
        """Clear the console for better readability."""
        Engine.Log("\033c", end="")