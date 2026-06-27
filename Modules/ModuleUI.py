from tkinter import ttk

class ModuleUI:
    def __init__(self, parent, task):
        self.parent = parent
        self.task = task
        self.frame = ttk.Frame(parent)
        self.frame.columnconfigure(0, weight=1)

    def widget(self):
        return self.frame

    def apply(self):
        pass
