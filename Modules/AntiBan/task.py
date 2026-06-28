from Services.Logger import Logger
from Tasks.Task import Task


class AntiBanTask(Task):
    def __init__(self, path):
        super().__init__(path)

        self.enable = self.settings.get("enable", False)
        self.humanize_mouse = self.settings.get("humanize_mouse", True)
        self.humanize_keyboard = self.settings.get("humanize_keyboard", True)

        self.camera_chance = self.settings.get("camera_chance", 50)
        self.camera_delay = self.settings.get("camera_delay", 8)

        self.idle_chance = self.settings.get("idle_chance", 30)
        self.idle_delay = self.settings.get("idle_delay", 3)

        self.active_chance = self.settings.get("active_chance", 20)
        self.active_delay = self.settings.get("active_delay", 15)
