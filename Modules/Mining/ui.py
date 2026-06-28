import tkinter as tk
from tkinter import ttk

from Modules.ModuleUI import ModuleUI
from Services.ActionFactory import ActionFactory


class TaskUI(ModuleUI):
    def __init__(self, parent, task):
        super().__init__(parent, task)

        # ---------------------------------------------------------
        # Resolve actions
        # ---------------------------------------------------------
        self.miningAction = ActionFactory.FindByName(self.actions, "mine")
        self.stashAction = ActionFactory.FindByName(self.actions, "stash")

        # ---------------------------------------------------------
        # Tk Variables
        # ---------------------------------------------------------
        self.enable_stash = tk.BooleanVar(value=self.stashAction.active or False)

        self.numeric_vars = {
            "Mining Delay (sec.)": tk.IntVar(value=self.miningAction.delay or 999),
            "Stash Delay (sec.)": tk.IntVar(value=self.stashAction.delay or 999),
        }

        # ---------------------------------------------------------
        # Variable Traces (auto-update task)
        # ---------------------------------------------------------
        self.enable_stash.trace_add("write", self._on_bool_changed)

        for var in self.numeric_vars.values():
            var.trace_add("write", self._on_numeric_changed)

        # ---------------------------------------------------------
        # Mining Settings UI
        # ---------------------------------------------------------
        settings = ttk.LabelFrame(self.frame, text="Mining Settings")
        settings.grid(row=0, column=0, sticky="nw", padx=5, pady=5)

        settings.columnconfigure(0, weight=0)
        settings.columnconfigure(1, weight=0, minsize=80)

        # Checkbox
        ttk.Checkbutton(
            settings, text="Enable Stashing", variable=self.enable_stash
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(2, 8))

        # Numeric Inputs
        row_index = 1
        for label_text, var in self.numeric_vars.items():
            ttk.Label(settings, text=label_text).grid(
                row=row_index, column=0, sticky="w", pady=2
            )
            ttk.Entry(settings, textvariable=var, width=6).grid(
                row=row_index, column=1, sticky="w"
            )
            row_index += 1

    # ---------------------------------------------------------
    # Callbacks
    # ---------------------------------------------------------

    def _on_bool_changed(self, *args):
        # Update action
        self.stashAction.active = self.enable_stash.get()

        # Regenerate configs
        self.task.configs["actions"] = [a.to_dict() for a in self.actions]

        # Save
        self.task.save()

    def _on_numeric_changed(self, *args):
        # Update delays
        self.miningAction.delay = self.numeric_vars["Mining Delay (sec.)"].get()
        self.stashAction.delay = self.numeric_vars["Stash Delay (sec.)"].get()

        # Regenerate configs
        self.task.configs["actions"] = [a.to_dict() for a in self.actions]

        # Save
        self.task.save()
