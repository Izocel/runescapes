"""
Auto‑clicker and key‑press automation script.

This script repeatedly performs:
1. A timed mouse click (used here for mining actions)
2. A periodic keyboard press (used here for stashing)

Delays include randomization to mimic human‑like behavior.
"""

import time
import random
from datetime import datetime
import keyboard
import mouse

# --- Configuration constants ---
CLICK_DELAY_SEC = 25          # Base delay between mouse clicks

KEY_PRESS_DELAY_SEC = 120     # Minimum delay between key presses
STASH_KEY = "num 0"          # Key to press periodically


def random_range(min_val: float = 1.0, max_val: float = 5.0) -> float:
    """
    Return a random float between min_val and max_val.

    Parameters:
        min_val (float): Lower bound of the random range.
        max_val (float): Upper bound of the random range.

    Returns:
        float: A random number within the given range.
    """
    return random.uniform(min_val, max_val)


def mouse_click(button: str = "left") -> None:
    """
    Perform a mouse click using the specified button.

    Parameters:
        button (str): Mouse button to click ("left", "right", etc.).
    """
    mouse.click(button)


def press_key(key: str) -> None:
    """
    Press and release a keyboard key with a small randomized delay.

    Parameters:
        key (str): The key to press (e.g., "num 0", "space", "a").
    """
    keyboard.press(key)
    time.sleep(random_range(0.20, 0.80))  # Human‑like key hold duration
    keyboard.release(key)

def delay_passed(last_time: float, delay: float) -> bool:
    """
    Check whether the required delay has passed since last_time.

    Parameters:
        last_time (float): Timestamp of the last action (seconds since epoch).
        delay (float): Required delay in seconds.

    Returns:
        bool: True if enough time has passed, False otherwise.
    """
    now = time.time()
    return last_time == 0 or delay <= 0 or (now - last_time) >= delay


def main() -> None:
    """
    Main automation loop.

    Repeatedly:
    - Waits a randomized delay
    - Performs a mouse click
    - Periodically presses a keyboard key
    """
    last_keyboard_time = 0

    while True:
        # Randomized wait before each click
        wait_time = CLICK_DELAY_SEC + random_range(0.5, 1.0)
        print(f"[INFO] Waiting {wait_time:.2f}s before next click...")
        time.sleep(wait_time)

        # Perform mouse click
        print("[ACTION] Mouse click for mining")
        mouse_click()

        # Perform periodic key press
        if delay_passed(last_keyboard_time, KEY_PRESS_DELAY_SEC):
            last_keyboard_time = time.time()
            print("[ACTION] Pressing stash key")
            press_key(STASH_KEY)


if __name__ == "__main__":
    main()
