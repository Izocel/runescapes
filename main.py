from Engine import Engine

# --- Configuration variables ---
MINING_KEY = "left"             # Key to press for mining (e.g., "mouse left" for left-click)
MINING_DELAY = 25               # Base delay between mouse clicks for mining
LAST_MINING_CLICK_TIME = 0      # Timestamp of the last mining click

STASH_KEY = "num 0"             # Key to press for stashing (e.g., "num 0" for Numpad 0)
STASH_DELAY = 120               # Base delay between key presses for stashing
LAST_STASH_PRESS_TIME = 0       # Timestamp of the last stash key press


def main() -> None:
    LAST_STASH_PRESS_TIME = 0

    while True:
        # Randomized wait before each loop to randomize all actions and avoid detection
        Engine.LoopSleep()

        ## Clean the console for better readability of logs
        Engine.ClearConsole()
        Engine.Log("Waiting for the next action...")

        # Check if it's time to click for mining
        if Engine.DelayPassed(LAST_MINING_CLICK_TIME, MINING_DELAY):
            Engine.Log("Mouse click for mining")
            Engine.KeyPress(MINING_KEY)
            LAST_MINING_CLICK_TIME = Engine.CurrentTimeStamp()

        # Check if it's time to press the stash key
        if Engine.DelayPassed(LAST_STASH_PRESS_TIME, STASH_DELAY):
            Engine.Log("Pressing stash key")
            Engine.KeyPress(STASH_KEY)
            LAST_STASH_PRESS_TIME = Engine.CurrentTimeStamp()

if __name__ == "__main__":
    main()
