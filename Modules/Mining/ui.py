import tkinter as tk
from tkinter import ttk


class MiningUI:
    def __init__(self, parent, task):
        self.task = task
        self.frame = ttk.Frame(parent)

        cfg = task.configs
        actions = cfg["actions"]
        settings = cfg["settings"]

        ttk.Label(
            self.frame,
            text="Mining Settings",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=5)

        # Mining delay
        ttk.Label(self.frame, text="Mining Delay (sec.):").pack(anchor="w")
        self.mine_delay = tk.IntVar(value=actions["mine"]["delay"])
        ttk.Entry(self.frame, textvariable=self.mine_delay).pack(fill="x", padx=5)

        # Stash delay
        ttk.Label(self.frame, text="Stash Delay (sec.):").pack(anchor="w")
        self.stash_delay = tk.IntVar(value=actions["stash"]["delay"])
        ttk.Entry(self.frame, textvariable=self.stash_delay).pack(fill="x", padx=5)

        # Stashing toggle
        self.stashing_var = tk.BooleanVar(value=settings.get("stashing", True))
        ttk.Checkbutton(
            self.frame,
            text="Enable Stashing",
            variable=self.stashing_var
        ).pack(anchor="w", padx=5, pady=5)

    # ---------------------------------------------------------
    # Apply UI → configs.json
    # ---------------------------------------------------------
    def apply(self):
        cfg = self.task.configs

        cfg["actions"]["mine"]["delay"] = self.mine_delay.get()
        cfg["actions"]["stash"]["delay"] = self.stash_delay.get()
        cfg["settings"]["stashing"] = self.stashing_var.get()

        self.task.save_configs()

        # Rebuild callbacks
        self.task.__init__(self.task.module_path)

    def widget(self):
        return self.frame
