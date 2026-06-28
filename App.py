import tkinter as tk

from UI.Scheduler import Scheduler


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RuneScape Automation Tool")
        self.geometry("900x650")

        scheduler = Scheduler(self)
        scheduler.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
