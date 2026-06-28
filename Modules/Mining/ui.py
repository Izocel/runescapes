import tkinter as tk
from tkinter import ttk

from Modules.ModuleUI import ModuleUI
from Services.ActionFactory import ActionFactory


class TaskUI(ModuleUI):
    def __init__(self, parent, task, configs):
        super().__init__(parent, task, configs)

        settings = ttk.LabelFrame(self.frame, text="Mining Settings")
        settings.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        settings.columnconfigure(1, weight=1)

        self.miningAction = ActionFactory.FindByName(self.actions, "mine")
        self.mining_delay = tk.IntVar(value=self.miningAction.delay or 999)

        self.stashAction = ActionFactory.FindByName(self.actions, "stash")
        self.stash_delay = tk.IntVar(value=self.stashAction.delay or 999)
        self.enable_stash = tk.BooleanVar(value=self.stashAction.active or False)

        ttk.Label(settings, text="Mining Delay (sec.):").grid(
            row=0, column=0, sticky="w", pady=2
        )
        ttk.Entry(settings, textvariable=self.mining_delay, width=6).grid(
            row=0, column=1, sticky="w"
        )

        ttk.Label(settings, text="Stash Delay (sec.):").grid(
            row=1, column=0, sticky="w", pady=2
        )
        ttk.Entry(settings, textvariable=self.stash_delay, width=6).grid(
            row=1, column=1, sticky="w"
        )

        ttk.Checkbutton(
            settings, text="Enable Stashing", variable=self.enable_stash
        ).grid(row=2, column=0, sticky="w", pady=4)
