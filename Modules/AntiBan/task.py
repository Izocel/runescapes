import random
from Tasks.Task import Task
from Logger import Logger
from Engine import Engine
from ActionBuilder import build_basic_actions


class AntiBanTask(Task):
    def __init__(self, module_path, configs=None):
        super().__init__(module_path, configs)

        cfg = self.configs

        # Settings (driven by UI + module.json)
        settings = cfg.get("settings", {})

        self.enable = settings.get("enable", False)
        self.humanize_mouse = settings.get("humanize_mouse", True)
        self.humanize_keyboard = settings.get("humanize_keyboard", True)

        self.camera_chance = settings.get("camera_chance", 50)
        self.idle_chance = settings.get("idle_chance", 30)
        self.active_chance = settings.get("active_chance", 20)

        self.camera_delay = settings.get("camera_delay", 8)
        self.idle_delay = settings.get("idle_delay", 3)
        self.active_delay = settings.get("active_delay", 15)

        self.actions = build_basic_actions(cfg.get("actions", []))

        # Simple throttling state
        self._last_run_ts = 0.0

    def on_start(self):
        Logger.Success("Anti-ban started")

    def on_stop(self):
        Logger.Error("Anti-ban stopped")

    def loop(self):
        if not self.enable:
            return

        # Throttle actions so delay settings have effect.
        # Since we don't have a real state machine from Engine here,
        # we approximate with: if any Engine action executes, treat as active.
        import time

        now = time.time()
        if self._last_run_ts and (now - self._last_run_ts) < (self.active_delay / 1.0):
            return

        for action in self.actions:
            chance = getattr(action, "chance", 1.0)
            if random.random() <= chance:
                # Additional gate based on chance sliders.
                # camera_move actions are treated as camera chances.
                name = getattr(action, "name", "")
                if name == "camera_move":
                    if random.randint(1, 100) > int(self.camera_chance):
                        continue

                Engine.RunAction(action)
                self._last_run_ts = now

