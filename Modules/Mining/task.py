from Tasks.Task import Task
from Logger import Logger
from Engine import Engine


class MiningTask(Task):
    def __init__(self, module_path, configs=None):
        super().__init__(module_path, configs)

        cfg = self.configs
        actions = cfg["actions"]

        # Build callbacks
        self.mine_action = lambda: Engine.Action(actions["mine"])
        self.stash_action = lambda: Engine.Action(actions["stash"])

        # Settings
        self.stashing = cfg["settings"].get("stashing", True)

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------
    def on_start(self):
        Logger.Success("Mining task started")

    def on_stop(self):
        Logger.Error("Mining task stopped")

    # ---------------------------------------------------------
    # Main Loop
    # ---------------------------------------------------------
    def loop(self):
        # Mine ore
        self.mine_action()

        # Stash ore
        if self.stashing:
            self.stash_action()
