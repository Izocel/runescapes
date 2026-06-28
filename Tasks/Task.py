import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from Classes.Actions import Action
from Classes.Constants import MODULE_CONFIG_FILENAME
from Services.ActionFactory import ActionFactory
from Services.Logger import Logger


@dataclass
class Task(ABC):
    path: str
    state: str = "idle"
    running: bool = False
    info: Dict[str, str] = field(default_factory=dict)
    configs: Dict[str, str] = field(default_factory=dict)
    settings: Dict[str, str] = field(default_factory=dict)
    context: Dict[str, str] = field(default_factory=dict)
    actions: List[Action] = field(default_factory=list)
    subtasks: List["Task"] = field(default_factory=list)

    def __post_init__(self):
        self.lodad()

    def reset(self):
        """Stops the task if it is running and resets it to its initial state."""
        if self.running:
            self.stop()
        self.state = "idle"
        self.running = False
        self.context = {}

    # ---------------------------------------------------------
    # Config loading / saving
    # ---------------------------------------------------------
    def lodad(self):
        """Load the configs file and parse the configs, settings, and actions."""
        if self.path is None:
            raise ValueError("Task path is not set. Cannot load configs.")

        config_path = os.path.join(self.path, MODULE_CONFIG_FILENAME)

        with open(config_path, "r") as f:
            data = json.load(f)

        self.info = data
        self.configs = (
            data["configs"] if "configs" in data else {"settings": {}, "actions": []}
        )

        # Ensure required keys exist
        self.configs.setdefault("settings", {})
        self.configs.setdefault("actions", [])

        self.settings = self.configs["settings"]
        self.actions = ActionFactory.Create(self.configs["actions"])

    def save(self, new_configs=None):
        """Save the current configs to the configs file."""
        if self.path is None:
            raise ValueError("Task path is not set. Cannot save configs.")

        if new_configs:
            self.configs = new_configs

        config_path = os.path.join(self.path, MODULE_CONFIG_FILENAME)
        self.info["configs"] = self.configs

        with open(config_path, "w") as f:
            json.dump(self.info, f, indent=2)

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
        self.reset()
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
        self.reset()

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
    def on_start(self):
        """Handle the start event."""
        pass

    def on_stop(self):
        """Handle the stop event."""
        pass

    def loop(self):
        """Handle the loop event."""
        pass
