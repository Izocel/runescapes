import tkinter as tk
from tkinter import ttk

from Modules.Bank.task import BANKS
from Modules.ModuleUI import ModuleUI


class TaskUI(ModuleUI):
    def __init__(self, parent, task):
        super().__init__(parent, task)

        stg = self.settings

        bank_key = stg.get("bank", "auto")
        self.bank = BANKS.get(bank_key, BANKS["auto"])

        self.enabled = tk.BooleanVar(value=stg.get("enable", False))
        self.bank_key_var = tk.StringVar(value=bank_key)

        settings = ttk.LabelFrame(self.frame, text="Bank Settings")
        settings.grid(row=0, column=0, sticky="nw", padx=5, pady=5)

        ttk.Checkbutton(
            settings,
            text="Enable Bank Task",
            variable=self.enabled,
            command=self.on_enable_toggle,
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=2)

        ttk.Label(settings, text="Select Bank:").grid(
            row=1, column=0, sticky="w", pady=(10, 2)
        )

        bank_combo = ttk.Combobox(
            settings,
            textvariable=self.bank_key_var,
            values=list(BANKS.keys()),
            state="readonly",
            width=20,
        )
        bank_combo.grid(row=1, column=1, sticky="w", pady=(10, 2))
        bank_combo.bind("<<ComboboxSelected>>", self.on_bank_change)

        self.bank_combobox = bank_combo

    def on_enable_toggle(self):
        self.settings["enable"] = self.enabled.get()
        # self.task.save()

    def on_bank_change(self, event):
        new_key = self.bank_key_var.get()
        self.settings["bank"] = new_key
        self.bank = BANKS.get(new_key, BANKS["auto"])
        # self.task.save()
