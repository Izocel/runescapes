from Tasks.Task import Task
from Logger import Logger
from Engine import Engine
from ActionBuilder import build_basic_actions


class MiningTask(Task):
    def __init__(self, module_path, configs=None):
        super().__init__(module_path, configs)

        cfg = self.configs
        # Convert configs actions into BasicAction instances.
        # Actions are already in the desired order in configs.
        self.actions = build_basic_actions(cfg.get("actions", []))

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
        for action in self.actions:
            Engine.RunAction(action)

