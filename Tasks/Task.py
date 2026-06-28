import json
import os
from abc import ABC, abstractmethod

from Classes.Constants import MODULE_CONFIG_FILENAME
from Services.ActionFactory import ActionFactory


class Task(ABC):
    def __init__(self, path=None):
        self.path = path
        self.info = {}

        self.configs = {}
        self.settings = {}
        self.actions = []
        self.subtasks = []

        self.running = False
        self.state = "idle"
        self.context = {}

        if path:
            self.load_configs()

    # ---------------------------------------------------------
    # Config loading / saving
    # ---------------------------------------------------------
    def load_configs(self):
        """Load the configs file and parse the configs, settings, and actions."""
        config_path = os.path.join(self.path, MODULE_CONFIG_FILENAME)

        with open(config_path, "r") as f:
            data = json.load(f)

        self.info = data
        self.configs = data.get("configs", {})
        self.settings = self.configs.get("settings", {})
        self.actions = ActionFactory.Create(self.configs.get("actions", []))

    def save_configs(self):
        """Save the current configs to the configs file."""
        config_path = os.path.join(self.path, MODULE_CONFIG_FILENAME)
        self.info["configs"] = self.configs

        with open(config_path, "w") as f:
            json.dump(self.info, f, indent=4)

    # ---------------------------------------------------------
    # Subtasks
    # ---------------------------------------------------------
    def add_subtask(self, task):
        """Add a subtask to the current task."""
        task.context = self.context
        self.subtasks.append(task)

    # ---------------------------------------------------------
    # State machine
    # ---------------------------------------------------------
    def set_state(self, new_state):
        """Set the state of the task and trigger the on_state_change event."""
        old = self.state
        self.state = new_state
        self.on_state_change(old, new_state)

    def on_state_change(self, old, new):
        """Handle the state change event."""
        pass

    # ---------------------------------------------------------
    # Lifecycle
    # ---------------------------------------------------------
    def start(self):
        """Start the task and its subtasks."""
        self.running = True
        self.set_state("starting")
        self.on_start()
        for t in self.subtasks:
            t.start()
        self.set_state("running")

    def stop(self):
        """Stop the task and its subtasks."""
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
        """Loop through the task and its subtasks."""
        if self.running:
            self.loop()
            for t in self.subtasks:
                t.loop_all()

    # ---------------------------------------------------------
    # Abstract methods
    # ---------------------------------------------------------
    @abstractmethod
    def on_start(self):
        """Handle the start event."""
        pass

    @abstractmethod
    def on_stop(self):
        """Handle the stop event."""
        pass

    @abstractmethod
    def loop(self):
        """Handle the loop event."""
        pass
