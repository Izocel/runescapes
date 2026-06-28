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

        # Numeric fields grouped for looping
        self.numeric_vars = {
            "Mining Delay (sec.)": tk.IntVar(value=self.miningAction.delay or 999),
            "Stash Delay (sec.)": tk.IntVar(value=self.stashAction.delay or 999),
        }

        # ---------------------------------------------------------
        # Mining Settings UI
        # ---------------------------------------------------------
        settings = ttk.LabelFrame(self.frame, text="Mining Settings")
        settings.grid(row=0, column=0, sticky="nw", padx=5, pady=5)

        settings.columnconfigure(0, weight=0)
        settings.columnconfigure(1, weight=0, minsize=80)

        # ---------------------------------------------------------
        # Checkbox
        # ---------------------------------------------------------
        ttk.Checkbutton(
            settings, text="Enable Stashing", variable=self.enable_stash
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(2, 8))

        # ---------------------------------------------------------
        # Numeric Inputs (Mining + Stash)
        # ---------------------------------------------------------
        row_index = 1
        for label_text, var in self.numeric_vars.items():
            ttk.Label(settings, text=label_text).grid(
                row=row_index, column=0, sticky="w", pady=2
            )
            ttk.Entry(settings, textvariable=var, width=6).grid(
                row=row_index, column=1, sticky="w"
            )
            row_index += 1
