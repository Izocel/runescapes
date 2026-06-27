import tkinter as tk
from tkinter import ttk


class ModuleUI:
    def __init__(self, parent, task):
        self.parent = parent
        self.task = task

        # Text widget handles scrolling natively
        self.text = tk.Text(
            parent,
            wrap="none",
            borderwidth=0,
            highlightthickness=0,
            bg="#ffffff"
        )
        self.text.pack(fill="both", expand=True)

        # Hidden scrollbar (functional but invisible)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=scrollbar.set)

        # Embed the actual module frame inside the text widget
        self.frame = ttk.Frame(self.text)
        self.text.window_create("end", window=self.frame)
        self.text.insert("end", "\n")  # allow scrolling past last widget

        # Allow module widgets to expand
        self.frame.columnconfigure(0, weight=1)

    def widget(self):
        return self.text

    def apply(self):
        pass
