import random
from Tasks.Task import Task
from Logger import Logger
from Engine import Engine


class AntiBanTask(Task):
    def __init__(self, module_path, configs=None):
        super().__init__(module_path, configs)

        cfg = self.configs

        # Settings
        settings = cfg.get("settings", {})
        
        self.enabled = settings.get("enabled", True)
        self.humanize_mouse = settings.get("humanize_mouse", True)
        self.humanize_keyboard = settings.get("humanize_keyboard", True)

        # Chances
        chances = cfg["chances"]
        self.camera_chance = chances["camera"]
        self.idle_chance = chances["idle"]
        self.active_chance = chances["active"]

        # Actions (list of objects with `name`)
        actions = cfg["actions"]
        actions_by_name = {a.get("name"): a for a in actions}

        self.camera_action = lambda: Engine.Action(actions_by_name["camera_move"])
        self.idle_action = lambda: Engine.Action(actions_by_name["idle_behavior"])
        self.active_action = lambda: Engine.Action(actions_by_name["active_behavior"])


    def on_start(self):
        Logger.Success("Anti-ban started")

    def on_stop(self):
        Logger.Error("Anti-ban stopped")

    def loop(self):
        if not self.enabled:
            return

        if random.random() < self.camera_chance and self.humanize_mouse:
            Logger.Action("Anti-ban: camera movement")
            self.camera_action()

        if random.random() < self.idle_chance:
            Logger.Action("Anti-ban: idle behavior")
            self.idle_action()

        if random.random() < self.active_chance and self.humanize_keyboard:
            Logger.Action("Anti-ban: active behavior")
            self.active_action()
