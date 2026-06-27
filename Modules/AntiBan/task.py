import random
from Tasks.Task import Task
from Logger import Logger
from Engine import Engine


class AntiBanTask(Task):
    def __init__(self, module_path):
        super().__init__(module_path)

        cfg = self.configs

        chances = cfg["chances"]
        self.camera_chance = chances["camera"]
        self.idle_chance = chances["idle"]
        self.active_chance = chances["active"]

        actions = cfg["actions"]
        self.camera_action = lambda: Engine.Action(actions["camera_move"])
        self.idle_action = lambda: Engine.Action(actions["idle_behavior"])
        self.active_action = lambda: Engine.Action(actions["active_behavior"])

    def on_start(self):
        Logger.Success("Anti-ban module started")

    def on_stop(self):
        Logger.Error("Anti-ban module stopped")

    def loop(self):
        if random.random() < self.camera_chance:
            Logger.Action("Anti-ban: camera movement")
            # self.camera_action()

        if random.random() < self.idle_chance:
            Logger.Action("Anti-ban: idle behavior")
            # self.idle_action()

        if random.random() < self.active_chance:
            Logger.Action("Anti-ban: active behavior")
            # self.active_action()
