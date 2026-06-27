import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

from Modules.loader import TASK_REGISTRY, TASK_UI_REGISTRY
from Logger import Logger
import threading
import time


class Scheduler(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.running = False
        self.task = None
        self.task_ui = None
        self.active_module = None
        self.icons = {}

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)   # top bar
        self.rowconfigure(1, weight=0)   # console
        self.rowconfigure(2, weight=0)   # console buttons
        self.rowconfigure(3, weight=0)   # tabs
        self.rowconfigure(4, weight=0)   # separator
        self.rowconfigure(5, weight=1)   # module panel

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Tab.TButton",
                        background="#e6e6e6",
                        foreground="#000000",
                        padding=(14, 6),
                        relief="raised",
                        borderwidth=1)
        style.map("Tab.TButton",
                  background=[("active", "#dcdcdc")])

        style.configure("TabActive.TButton",
                        background="#ffffff",
                        foreground="#000000",
                        padding=(14, 6),
                        relief="flat",
                        borderwidth=1)

        style.configure(".", background="#f2f2f2", foreground="#000000")
        style.configure("TFrame", background="#f2f2f2")
        style.configure("TLabelframe", background="#f2f2f2", foreground="#000000")
        style.configure("TLabelframe.Label", background="#f2f2f2", foreground="#000000")
        style.configure("TLabel", background="#f2f2f2", foreground="#000000")
        style.configure("TButton", background="#e6e6e6", foreground="#000000", padding=6)
        style.map("TButton", background=[("active", "#d9d9d9")])

        topbar = ttk.Frame(self)
        topbar.grid(row=0, column=0, sticky="ew", pady=5, padx=10)
        topbar.columnconfigure(1, weight=1)

        self.toggle_btn = ttk.Button(topbar, text="Start", command=self.toggle_module)
        self.toggle_btn.grid(row=0, column=0, sticky="w")

        ttk.Label(
            topbar,
            text="RuneScape Automation Tool",
            font=("Segoe UI", 16, "bold")
        ).grid(row=0, column=1, sticky="n")

        self.status = ttk.Label(topbar, text="Status: Idle")
        self.status.grid(row=0, column=2, sticky="e")

        console_frame = ttk.LabelFrame(self, text="Console")
        console_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 0))
        console_frame.rowconfigure(0, weight=1)
        console_frame.columnconfigure(0, weight=1)

        self.log_text = tk.Text(
            console_frame,
            height=10,
            bg="#ffffff",
            fg="#000000",
            insertbackground="black",
            wrap="word",
            borderwidth=1,
            highlightthickness=0,
            state="disabled"
        )
        self.log_text.grid(row=0, column=0, sticky="nsew")

        self.log_text.tag_config("INFO", foreground="#000000")
        self.log_text.tag_config("ACTION", foreground="#007acc")
        self.log_text.tag_config("ERROR", foreground="#cc0000")
        self.log_text.tag_config("SUCCESS", foreground="#008000")
        self.log_text.tag_config("DEBUG", foreground="#b8860b")

        Logger.gui_callback = self.gui_log
        Logger.copy_callback = self.copy_log
        Logger.gui_clear_callback = self.clear_log

        console_buttons = ttk.Frame(self)
        console_buttons.grid(row=2, column=0, sticky="e", padx=10, pady=(0, 5))

        ttk.Button(console_buttons, text="Copy Console", command=self.copy_log).pack(side="right", padx=5)
        ttk.Button(console_buttons, text="Clear Console", command=self.clear_log).pack(side="right")

        tab_frame = ttk.Frame(self)
        tab_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(5, 0))

        self.module_buttons = {}

        for module_name, (TaskClass, module_path) in TASK_REGISTRY.items():
            icon = self.load_icon(module_path)
            btn = ttk.Button(
                tab_frame,
                text=f"  {module_name}",
                image=icon,
                compound="left",
                style="Tab.TButton",
                command=lambda m=module_name: self.switch_module(m)
            )
            btn.pack(side="left", padx=(0, 4))
            self.module_buttons[module_name] = btn

        separator = ttk.Separator(self, orient="horizontal")
        separator.grid(row=4, column=0, sticky="ew")

        self.panel_container = ttk.Frame(self)
        self.panel_container.grid(row=5, column=0, sticky="nsew", padx=10, pady=5)
        self.panel_container.columnconfigure(0, weight=1)
        self.panel_container.rowconfigure(0, weight=1)

        first_module = list(TASK_REGISTRY.keys())[0]
        self.switch_module(first_module)

    def load_icon(self, module_path):
        icon_path = os.path.join(module_path, "icon.png")

        if os.path.exists(icon_path):
            img = Image.open(icon_path).resize((18, 18))
            tk_img = ImageTk.PhotoImage(img)
            self.icons[module_path] = tk_img
            return tk_img

        return None

    def switch_module(self, module_name):
        for name, btn in self.module_buttons.items():
            btn.config(style="TabActive.TButton" if name == module_name else "Tab.TButton")

        for widget in self.panel_container.winfo_children():
            widget.destroy()

        self.active_module = module_name

        TaskClass, module_path = TASK_REGISTRY[module_name]
        self.task = TaskClass(module_path=module_path)

        UIClass = TASK_UI_REGISTRY.get(module_name)
        if UIClass:
            self.task_ui = UIClass(self.panel_container, self.task)
            widget = self.task_ui.widget()
            widget.grid(row=0, column=0, sticky="nsew")

    def gui_log(self, msg, tag="INFO"):
        self.log_text.config(state="normal")
        self.log_text.insert("end", msg + "\n", tag)
        self.log_text.config(state="disabled")
        self.log_text.see("end")

    def copy_log(self):
        text = self.log_text.get("1.0", "end").strip()
        self.clipboard_clear()
        self.clipboard_append(text)

    def clear_log(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")

    def toggle_module(self):
        if not self.running:
            self.start_module()
        else:
            self.stop_module()

    def start_module(self):
        if self.task_ui:
            self.task_ui.apply()

        self.task.start()
        self.running = True

        self.toggle_btn.config(text="Stop")
        self.status.config(text=f"Status: Module Running ({self.active_module})")

        threading.Thread(target=self.module_loop, daemon=True).start()

    def stop_module(self):
        self.running = False
        if self.task:
            self.task.stop()

        self.toggle_btn.config(text="Start")
        self.status.config(text="Status: Idle")

    def module_loop(self):
        while self.running and self.task.running:
            self.task.loop_all()
            time.sleep(0.05)
