import tkinter as tk
from tkinter import ttk

from Classes.Actions import Action
from Modules.ModuleUI import ModuleUI
from Services.ActionFactory import ActionFactory


class TaskUI(ModuleUI):
    def __init__(self, parent, task):
        super().__init__(parent, task)
        stg = self.settings

        # -------------------------
        # Tk Variables
        # -------------------------
        self.enabled = tk.BooleanVar(value=stg.get("enable", False))
        self.mouseEnabled = tk.BooleanVar(value=stg.get("humanize_mouse", False))
        self.keyboardEnabled = tk.BooleanVar(value=stg.get("humanize_keyboard", False))

        # Numeric fields stored in a dict for easy looping
        self.numeric_vars = {
            "Camera Delay (sec.)": tk.IntVar(value=stg.get("camera_delay", 999)),
            "Idle Delay (sec.)": tk.IntVar(value=stg.get("idle_delay", 999)),
            "Active Delay (sec.)": tk.IntVar(value=stg.get("active_delay", 999)),
            "Camera Chance (%)": tk.IntVar(value=stg.get("camera_chance", 0)),
            "Idle Chance (%)": tk.IntVar(value=stg.get("idle_chance", 0)),
            "Active Chance (%)": tk.IntVar(value=stg.get("active_chance", 0)),
        }

        # -------------------------
        # Variable Traces
        # -------------------------
        self.enabled.trace_add("write", self._on_bool_changed)
        self.mouseEnabled.trace_add("write", self._on_bool_changed)
        self.keyboardEnabled.trace_add("write", self._on_bool_changed)

        for var in self.numeric_vars.values():
            var.trace_add("write", self._on_numeric_changed)

        # ============================================================
        # ANTI-BAN SETTINGS
        # ============================================================
        settings = ttk.LabelFrame(self.frame, text="Anti-Ban Settings")
        settings.grid(row=0, column=0, sticky="nw", padx=5, pady=5)

        settings.columnconfigure(0, weight=0)
        settings.columnconfigure(1, weight=0, minsize=80)

        # --- Checkboxes ---
        for i, (text, var) in enumerate(
            [
                ("Enable Anti-Ban", self.enabled),
                ("Humanize Mouse", self.mouseEnabled),
                ("Humanize Keyboard", self.keyboardEnabled),
            ]
        ):
            ttk.Checkbutton(settings, text=text, variable=var).grid(
                row=i, column=0, columnspan=2, sticky="w", pady=2
            )

        # ============================================================
        # NUMERIC INPUTS (Delays + Chances)
        # ============================================================

        row_index = 3
        for label_text, var in self.numeric_vars.items():
            pady = (10, 2) if row_index == 3 else 2
            ttk.Label(settings, text=label_text).grid(
                row=row_index, column=0, sticky="w", pady=pady
            )
            ttk.Entry(settings, textvariable=var, width=6).grid(
                row=row_index, column=1, sticky="w"
            )
            row_index += 1

    # -------------------------
    # Callbacks
    # -------------------------

    def _on_bool_changed(self, *args):
        self.settings["enable"] = self.enabled.get()
        self.settings["humanize_mouse"] = self.mouseEnabled.get()
        self.settings["humanize_keyboard"] = self.keyboardEnabled.get()
        self.task.save()

    def _on_numeric_changed(self, *args):
        for label_text, var in self.numeric_vars.items():
            key = (
                label_text.lower()
                .replace(" ", "_")
                .replace("(sec.)", "")
                .replace("(%)", "")
                .strip()
                .strip("_")
            )
            self.settings[key] = var.get()

        self.task.save()
