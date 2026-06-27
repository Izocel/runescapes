import tkinter as tk
from tkinter import ttk


class AntiBanUI:
    def __init__(self, parent, task):
        self.task = task
        self.frame = ttk.Frame(parent)

        cfg = task.configs
        actions = cfg["actions"]
        chances = cfg["chances"]
        settings = cfg["settings"]

        ttk.Label(
            self.frame,
            text="Anti-Ban Settings",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=5)

        # -----------------------------
        # SETTINGS
        # -----------------------------
        self.enabled = tk.BooleanVar(value=settings.get("enabled", True))
        ttk.Checkbutton(self.frame, text="Enable Anti-Ban", variable=self.enabled).pack(anchor="w")

        self.humanize_mouse = tk.BooleanVar(value=settings.get("humanize_mouse", True))
        ttk.Checkbutton(self.frame, text="Humanize Mouse", variable=self.humanize_mouse).pack(anchor="w")

        self.humanize_keyboard = tk.BooleanVar(value=settings.get("humanize_keyboard", True))
        ttk.Checkbutton(self.frame, text="Humanize Keyboard", variable=self.humanize_keyboard).pack(anchor="w")

        # -----------------------------
        # CHANCES
        # -----------------------------
        ttk.Label(self.frame, text="Camera Chance").pack(anchor="w")
        self.camera_chance = tk.DoubleVar(value=chances["camera"])
        ttk.Scale(self.frame, from_=0.0, to=1.0, variable=self.camera_chance).pack(fill="x", padx=5)

        ttk.Label(self.frame, text="Idle Chance").pack(anchor="w")
        self.idle_chance = tk.DoubleVar(value=chances["idle"])
        ttk.Scale(self.frame, from_=0.0, to=1.0, variable=self.idle_chance).pack(fill="x", padx=5)

        ttk.Label(self.frame, text="Active Chance").pack(anchor="w")
        self.active_chance = tk.DoubleVar(value=chances["active"])
        ttk.Scale(self.frame, from_=0.0, to=1.0, variable=self.active_chance).pack(fill="x", padx=5)

        # -----------------------------
        # ACTION DELAYS
        # -----------------------------
        ttk.Label(self.frame, text="Camera Delay (sec.)").pack(anchor="w")
        self.camera_delay = tk.IntVar(value=actions["camera_move"]["delay"])
        ttk.Entry(self.frame, textvariable=self.camera_delay).pack(fill="x", padx=5)

        ttk.Label(self.frame, text="Idle Delay (sec.)").pack(anchor="w")
        self.idle_delay = tk.IntVar(value=actions["idle_behavior"]["delay"])
        ttk.Entry(self.frame, textvariable=self.idle_delay).pack(fill="x", padx=5)

        ttk.Label(self.frame, text="Active Delay (sec.)").pack(anchor="w")
        self.active_delay = tk.IntVar(value=actions["active_behavior"]["delay"])
        ttk.Entry(self.frame, textvariable=self.active_delay).pack(fill="x", padx=5)

    def apply(self):
        cfg = self.task.configs

        # SETTINGS
        cfg["settings"]["enabled"] = self.enabled.get()
        cfg["settings"]["humanize_mouse"] = self.humanize_mouse.get()
        cfg["settings"]["humanize_keyboard"] = self.humanize_keyboard.get()

        # CHANCES
        cfg["chances"]["camera"] = self.camera_chance.get()
        cfg["chances"]["idle"] = self.idle_chance.get()
        cfg["chances"]["active"] = self.active_chance.get()

        # ACTION DELAYS
        cfg["actions"]["camera_move"]["delay"] = self.camera_delay.get()
        cfg["actions"]["idle_behavior"]["delay"] = self.idle_delay.get()
        cfg["actions"]["active_behavior"]["delay"] = self.active_delay.get()

        self.task.save_configs()
        self.task.__init__(self.task.module_path)

    def widget(self):
        return self.frame
