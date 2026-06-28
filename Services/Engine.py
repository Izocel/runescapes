import datetime
import random
import time

import keyboard
from human_mouse import MouseController
from pyHM import mouse

from Classes.Actions import Action
from Services.Logger import Logger

MC = MouseController(always_zigzag=True)


class Engine:
    LOOP_MIN_DELAY = 1.0  # Minimum delay between loops in seconds
    LOOP_MAX_DELAY = 3.0  # Maximum delay between loops in seconds
    MOUSE_MIN_DELAY = 0.2  # Minimum delay for mouse actions in seconds
    MOUSE_MAX_DELAY = 0.5  # Maximum delay for mouse actions in seconds
    KEY_MIN_DELAY = 0.2  # Minimum delay for keyboard actions in seconds
    KEY_MAX_DELAY = 0.8  # Maximum delay for keyboard actions in seconds
    MOUSE_SPEED = 0.01  # Default speed factor for mouse movements (lower is faster)

    def __init__(self):
        pass

    @staticmethod
    def Sleep(seconds: float = None) -> None:
        """Sleep for the specified number of seconds."""
        if seconds is not None:
            time.sleep(seconds)

    @staticmethod
    def LoopSleep() -> None:
        """Sleep for a randomized delay between loops."""
        total_delay = Engine.RandomFloat(Engine.LOOP_MIN_DELAY, Engine.LOOP_MAX_DELAY)
        Engine.Sleep(total_delay)

    @staticmethod
    def MouseWait(base_delay: float = None) -> None:
        """Wait for a randomized delay based on the base_delay and configured random range."""
        total_delay = (base_delay or 0.0) + Engine.RandomFloat(
            Engine.MOUSE_MIN_DELAY, Engine.MOUSE_MAX_DELAY
        )
        Engine.Sleep(total_delay)

    @staticmethod
    def KeyWait(base_delay: float = None) -> None:
        """Wait for a randomized delay based on the base_delay and configured random range."""
        total_delay = (base_delay or 0.0) + Engine.RandomFloat(
            Engine.KEY_MIN_DELAY, Engine.KEY_MAX_DELAY
        )
        Engine.Sleep(total_delay)

    @staticmethod
    def MoveMouse(x: int, y: int, speed: float = None) -> None:
        """Move the MC to the specified coordinates with optional speed."""
        if x is not None and y is not None:
            MC.move(x, y, speed_factor=speed or Engine.MOUSE_SPEED)

    @staticmethod
    def MouseDown(
        button: str = "left", x: int = None, y: int = None, speed: float = None
    ) -> None:
        """Press and hold a mouse button at the specified coordinates (or current position if None)."""
        Engine.MoveMouse(x, y, speed)
        mouse.down(button=button)

    @staticmethod
    def MouseUp(
        button: str = "left", x: int = None, y: int = None, speed: float = None
    ) -> None:
        """Release a mouse button at the specified coordinates (or current position if None)."""
        Engine.MoveMouse(x, y, speed)
        mouse.up(button=button)

    @staticmethod
    def MouseClick(
        button: str = "left", x: int = None, y: int = None, speed: float = None
    ) -> None:
        """Perform a MC click at the specified coordinates (or current position if None)."""
        Engine.MouseDown(button=button, x=x, y=y, speed=speed)
        Engine.MouseWait()
        Engine.MouseUp(button=button, x=x, y=y, speed=speed)

    @staticmethod
    def MouseDrag(
        start_x: int = None,
        start_y: int = None,
        end_x: int = None,
        end_y: int = None,
        speed: float = None,
    ) -> None:
        """Perform a MC drag from (start_x, start_y) to (end_x, end_y) over the specified duration."""
        Engine.MouseDown(x=start_x, y=start_y, speed=speed)
        Engine.MouseWait()
        Engine.MouseUp(x=end_x, y=end_y, speed=speed)

    @staticmethod
    def KeyPress(key: str) -> None:
        """Press and release a keyboard key with a small randomized delay."""
        keyboard.press(key)
        Engine.KeyWait()
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
    def TimeSince(start: float = None) -> float:
        """Return the time elapsed since start."""
        return Engine.CurrentTimeStamp() - (start or 0.0)

    @staticmethod
    def DelayPassed(start: float = None, delay: float = None) -> bool:
        """Check if the specified delay has passed since `start`.

        Convention: if `start` is 0/None, treat as "never executed" and allow immediately.
        """
        return (
            (start is None)
            or (start <= 0)
            or (delay or 0.0) <= 0
            or Engine.TimeSince(start) >= (delay or 0.0)
        )

    @staticmethod
    def TryExecuteAction(action: Action) -> bool:
        """Execute the concrete action payload. Returns whether something executed."""
        x = action.x
        y = action.y
        key = action.key
        name = action.name
        speed = action.speed
        delay = action.delay
        active = action.active
        actionType = action.type
        lastExec = action.lastExec

        if not active:
            Logger.Info(f"Action '{name}' is inactive. Skipping execution.")
            return False

        if not Engine.DelayPassed(lastExec, delay or 0.0):
            return False

        if actionType == "mouse":
            Engine.MouseClick(x=x, y=y, speed=speed)
            Logger.Info(
                f"Mouse action '{name}' executed at ({x}, {y}) with speed {speed}"
            )
            return True

        if actionType == "keyboard":
            Engine.KeyPress(key)
            Logger.Info(f"Keyboard action '{name}' executed")
            return True

        if actionType == "delay":
            # For delay actions, action.delay is the sleep duration.
            if delay:
                Engine.Sleep(float(delay))
            return True

        Logger.Error(f"Unknown action type '{actionType}' for action '{name}'")
        return False

    @staticmethod
    def TryUpdateAction(action: Action) -> None:
        """Updates action lastExec / action.nextExec after a successful execution."""
        delay = action.delay
        now = Engine.CurrentTimeStamp()
        action.lastExec = now
        if delay:
            action.nextExec = now + float(delay)
