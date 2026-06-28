from Services.Engine import Engine
from Services.Logger import Logger
from Tasks.Task import Task


class MiningTask(Task):
    def __init__(self, path):
        super().__init__(path)

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------
    def on_start(self):
        Logger.Success("Mining-Task (started)")

    def on_stop(self):
        Logger.Error("Mining-Task (stopped)")

    # ---------------------------------------------------------
    # Main Loop
    # ---------------------------------------------------------
    def loop(self):
        for action in self.actions:
            if Engine.TryExecuteAction(action):
                Engine.TryUpdateAction(action)
