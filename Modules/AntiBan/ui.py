import tkinter as tk
from tkinter import ttk
from Modules.ModuleUI import ModuleUI


class TaskUI(ModuleUI):
    def __init__(self, parent, task, configs):
        super().__init__(parent, task, configs)

        settings = ttk.LabelFrame(self.frame, text="Anti-Ban Settings")
        settings.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        settings.columnconfigure(0, weight=1)

        self.enable_var = tk.BooleanVar(value=True)
        self.mouse_var = tk.BooleanVar(value=True)
        self.keyboard_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(settings, text="Enable Anti-Ban",
                        variable=self.enable_var).grid(row=0, column=0, sticky="w", pady=2)
        ttk.Checkbutton(settings, text="Humanize Mouse",
                        variable=self.mouse_var).grid(row=1, column=0, sticky="w", pady=2)
        ttk.Checkbutton(settings, text="Humanize Keyboard",
                        variable=self.keyboard_var).grid(row=2, column=0, sticky="w", pady=2)

        self.camera_chance = tk.IntVar(value=50)
        self.idle_chance = tk.IntVar(value=30)
        self.active_chance = tk.IntVar(value=20)

        ttk.Label(settings, text="Camera Chance").grid(row=3, column=0, sticky="w")
        ttk.Scale(settings, from_=0, to=100,
                  orient="horizontal",
                  variable=self.camera_chance).grid(row=4, column=0, sticky="ew", pady=3)

        ttk.Label(settings, text="Idle Chance").grid(row=5, column=0, sticky="w")
        ttk.Scale(settings, from_=0, to=100,
                  orient="horizontal",
                  variable=self.idle_chance).grid(row=6, column=0, sticky="ew", pady=3)

        ttk.Label(settings, text="Active Chance").grid(row=7, column=0, sticky="w")
        ttk.Scale(settings, from_=0, to=100,
                  orient="horizontal",
                  variable=self.active_chance).grid(row=8, column=0, sticky="ew", pady=3)

        delays = ttk.LabelFrame(self.frame, text="Delays")
        delays.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        delays.columnconfigure(1, weight=1)

        self.camera_delay = tk.IntVar(value=8)
        self.idle_delay = tk.IntVar(value=3)
        self.active_delay = tk.IntVar(value=15)

        ttk.Label(delays, text="Camera Delay (sec.):").grid(row=0, column=0, sticky="w", pady=2)
        ttk.Entry(delays, textvariable=self.camera_delay, width=6).grid(row=0, column=1, sticky="w")

        ttk.Label(delays, text="Idle Delay (sec.):").grid(row=1, column=0, sticky="w", pady=2)
        ttk.Entry(delays, textvariable=self.idle_delay, width=6).grid(row=1, column=1, sticky="w")

        ttk.Label(delays, text="Active Delay (sec.):").grid(row=2, column=0, sticky="w", pady=2)
        ttk.Entry(delays, textvariable=self.active_delay, width=6).grid(row=2, column=1, sticky="w")

    def apply(self):
        self.task.enable = self.enable_var.get()
        self.task.humanize_mouse = self.mouse_var.get()
        self.task.humanize_keyboard = self.keyboard_var.get()
        self.task.camera_chance = self.camera_chance.get()
        self.task.idle_chance = self.idle_chance.get()
        self.task.active_chance = self.active_chance.get()
        self.task.camera_delay = self.camera_delay.get()
        self.task.idle_delay = self.idle_delay.get()
        self.task.active_delay = self.active_delay.get()
