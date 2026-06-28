import json
import os
from abc import ABC, abstractmethod

from Services.ActionFactory import ActionFactory


class Task(ABC):
    def __init__(self, module_path=None, configs=None):
        self.running = False
        self.subtasks = []
        self.state = "idle"
        self.context = {}  # shared data for subtasks

        self.module_path = module_path
        self.module_info = {}
        self.configs = {}
        self.settings = {}
        self.actions = []

        # Load configs from module.json
        if module_path:
            self.load_configs()

    # ---------------------------------------------------------
    # Config loading / saving
    # ---------------------------------------------------------
    def load_configs(self):
        config_path = os.path.join(self.module_path, "module.json")

        with open(config_path, "r") as f:
            data = json.load(f)

        self.module_info = data
        self.configs = data.get("configs", {})
        self.settings = self.configs.get("settings", {})
        self.actions = ActionFactory.Create(self.configs.get("actions", []))

    def save_configs(self):
        config_path = os.path.join(self.module_path, "module.json")
        self.module_info["configs"] = self.configs

        with open(config_path, "w") as f:
            json.dump(self.module_info, f, indent=4)

    # ---------------------------------------------------------
    # Subtasks
    # ---------------------------------------------------------
    def add_subtask(self, task):
        task.context = self.context
        self.subtasks.append(task)

    # ---------------------------------------------------------
    # State machine
    # ---------------------------------------------------------
    def set_state(self, new_state):
        old = self.state
        self.state = new_state
        self.on_state_change(old, new_state)

    def on_state_change(self, old, new):
        pass

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------
    def start(self):
        self.running = True
        self.set_state("starting")
        self.on_start()
        for t in self.subtasks:
            t.start()
        self.set_state("running")

    def stop(self):
        self.running = False
        self.set_state("stopping")
        for t in self.subtasks:
            t.stop()
        self.on_stop()
        self.set_state("stopped")

    # ---------------------------------------------------------
    # Loop
    # ---------------------------------------------------------
    def loop_all(self):
        if self.running:
            self.loop()
            for t in self.subtasks:
                t.loop_all()

    # ---------------------------------------------------------
    # Abstract methods
    # ---------------------------------------------------------
    @abstractmethod
    def on_start(self):
        pass

    @abstractmethod
    def on_stop(self):
        pass

    @abstractmethod
    def loop(self):
        pass
