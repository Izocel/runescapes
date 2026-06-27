import tkinter as tk
from tkinter import ttk


class AntiBanUI:
    def __init__(self, parent, task):
        self.task = task
        self.frame = ttk.Frame(parent)

        cfg = task.configs
        actions = cfg["actions"]
        chances = cfg["chances"]

        ttk.Label(
            self.frame,
            text="Anti-Ban Settings",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=5)

        # -----------------------------
        # Chance sliders
        # -----------------------------
        ttk.Label(self.frame, text="Camera Movement Chance").pack(anchor="w")
        self.camera_chance = tk.DoubleVar(value=chances["camera"])
        ttk.Scale(self.frame, from_=0.0, to=1.0, variable=self.camera_chance).pack(fill="x", padx=5)

        ttk.Label(self.frame, text="Idle Behavior Chance").pack(anchor="w")
        self.idle_chance = tk.DoubleVar(value=chances["idle"])
        ttk.Scale(self.frame, from_=0.0, to=1.0, variable=self.idle_chance).pack(fill="x", padx=5)

        ttk.Label(self.frame, text="Active Behavior Chance").pack(anchor="w")
        self.active_chance = tk.DoubleVar(value=chances["active"])
        ttk.Scale(self.frame, from_=0.0, to=1.0, variable=self.active_chance).pack(fill="x", padx=5)

        # -----------------------------
        # Action delays
        # -----------------------------
        ttk.Label(self.frame, text="Camera Move Delay (ms)").pack(anchor="w")
        self.camera_delay = tk.IntVar(value=actions["camera_move"]["delay"])
        ttk.Entry(self.frame, textvariable=self.camera_delay).pack(fill="x", padx=5)

        ttk.Label(self.frame, text="Idle Behavior Delay (ms)").pack(anchor="w")
        self.idle_delay = tk.IntVar(value=actions["idle_behavior"]["delay"])
        ttk.Entry(self.frame, textvariable=self.idle_delay).pack(fill="x", padx=5)

        ttk.Label(self.frame, text="Active Behavior Delay (ms)").pack(anchor="w")
        self.active_delay = tk.IntVar(value=actions["active_behavior"]["delay"])
        ttk.Entry(self.frame, textvariable=self.active_delay).pack(fill="x", padx=5)

    # ---------------------------------------------------------
    # Apply → save → reload task
    # ---------------------------------------------------------
    def apply(self):
        cfg = self.task.configs

        # Update chances
        cfg["chances"]["camera"] = self.camera_chance.get()
        cfg["chances"]["idle"] = self.idle_chance.get()
        cfg["chances"]["active"] = self.active_chance.get()

        # Update delays
        cfg["actions"]["camera_move"]["delay"] = self.camera_delay.get()
        cfg["actions"]["idle_behavior"]["delay"] = self.idle_delay.get()
        cfg["actions"]["active_behavior"]["delay"] = self.active_delay.get()

        # Save to module.json
        self.task.save_configs()

        # Reload task so callbacks update
        self.task.__init__(self.task.module_path)

    def widget(self):
        return self.frame
