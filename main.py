from Engine import Engine

# --- Configuration variables ---
CLICK_DELAY_SEC = 25          # Base delay between mouse clicks for mining

STASH_KEY = "num 0"           # Key to press for stashing (e.g., "num 0" for Numpad 0)
KEY_PRESS_DELAY_SEC = 120     # Base delay between key presses for stashing


def main() -> None:
    LAST_STASH_PRESS_TIME = 0

    while True:
        # Randomized wait before each loop to randomize all actions and avoid detection
        Engine.LoopSleep()

        ## Clean the console for better readability of logs
        Engine.ClearConsole()

        # Wait for the click delay with added randomization
        Engine.Log("Mouse click for mining")
        Engine.MouseClick("left")

        # Check if it's time to press the stash key
        if Engine.DelayPassed(LAST_STASH_PRESS_TIME, KEY_PRESS_DELAY_SEC):
            Engine.Log("Pressing stash key")
            LAST_STASH_PRESS_TIME = Engine.CurrentTimeStamp()
            Engine.KeyPress(STASH_KEY)

if __name__ == "__main__":
    main()
