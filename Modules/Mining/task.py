from Services.ActionFactory import ActionFactory
from Services.Logger import Logger
from Tasks.Task import Task


class MiningTask(Task):
    def __init__(self, module_path, configs=None):
        super().__init__(module_path, configs)

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------
    def on_start(self):
        Logger.Success("---------------- Mining task started ----------------")

    def on_stop(self):
        Logger.Error("---------------- Mining task stopped ----------------")

    # ---------------------------------------------------------
    # Main Loop
    # ---------------------------------------------------------
    def loop(self):
        for action in self.actions:
            ActionFactory.RunAction(action)
