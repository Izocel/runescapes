import tkinter as tk
from tkinter import ttk
import threading
import time

from Modules.loader import TASK_REGISTRY, TASK_UI_REGISTRY
from Logger import Logger


class Scheduler(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.running = False
        self.task = None
        self.task_ui = None

        # --- Task Settings Panel ---
        settings_frame = ttk.LabelFrame(self, text="Task Settings")
        settings_frame.pack(fill="x", padx=10, pady=5)

        self.task_settings_container = ttk.Frame(settings_frame)
        self.task_settings_container.pack(fill="x")

        # --- Title ---
        ttk.Label(self, text="RuneScape Automation Tool",
                  font=("Segoe UI", 12, "bold")).pack(pady=10)

        # --- Task Selection ---
        ttk.Label(self, text="Select Task:").pack(pady=5)

        self.task_var = tk.StringVar()
        self.task_var.set(list(TASK_REGISTRY.keys())[0])

        self.task_menu = ttk.OptionMenu(
            self,
            self.task_var,
            self.task_var.get(),
            *TASK_REGISTRY.keys()
        )
        self.task_menu.pack(pady=5)

        self.task_var.trace_add("write", self.on_task_selected)

        # --- Start / Stop Buttons ---
        self.start_btn = ttk.Button(self, text="Start Bot", command=self.start_bot)
        self.start_btn.pack(pady=5)

        self.stop_btn = ttk.Button(self, text="Stop Bot", command=self.stop_bot, state="disabled")
        self.stop_btn.pack(pady=5)

        self.status = ttk.Label(self, text="Status: Idle")
        self.status.pack(pady=10)

        # --- Logging Window ---
        log_frame = ttk.LabelFrame(self, text="Log Output")
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = tk.Text(log_frame, height=10, state="disabled", wrap="word")
        self.log_text.pack(fill="both", expand=True)

        # Log color tags
        self.log_text.tag_config("INFO", foreground="#DDDDDD")
        self.log_text.tag_config("ACTION", foreground="#00FFFF")
        self.log_text.tag_config("ERROR", foreground="#FF5555")
        self.log_text.tag_config("SUCCESS", foreground="#55FF55")
        self.log_text.tag_config("DEBUG", foreground="#FFFF55")

        # --- Log Buttons ---
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Clear Log", command=Logger.Clear).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Copy Log", command=Logger.Copy).pack(side="left", padx=5)

        # Register Logger callbacks
        Logger.gui_callback = self.gui_log
        Logger.copy_callback = self.copy_log
        Logger.gui_clear_callback = self.clear_log

        # Load initial task UI
        self.on_task_selected()

    # ---------------------------------------------------------
    # Task UI Loader
    # ---------------------------------------------------------
    def on_task_selected(self, *args):
        # Clear previous UI
        for widget in self.task_settings_container.winfo_children():
            widget.destroy()

        task_name = self.task_var.get()

        # Create the task instance (logic only)
        TaskClass, module_path = TASK_REGISTRY[task_name]
        self.task = TaskClass(module_path=module_path)

        # Load the UI panel for this task
        UIClass = TASK_UI_REGISTRY.get(task_name)

        if UIClass:
            self.task_ui = UIClass(self.task_settings_container, self.task)
            self.task_ui.widget().pack(fill="x", padx=5, pady=5)
        else:
            self.task_ui = None

    # ---------------------------------------------------------
    # Logging
    # ---------------------------------------------------------
    def gui_log(self, formatted_message: str, tag: str = "INFO"):
        self.log_text.config(state="normal")
        self.log_text.insert("end", formatted_message + "\n", tag)
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def copy_log(self):
        text = self.log_text.get("1.0", "end").strip()
        self.clipboard_clear()
        self.clipboard_append(text)

    def clear_log(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")

    # ---------------------------------------------------------
    # Start / Stop Bot
    # ---------------------------------------------------------
    def start_bot(self):
        if not self.running:
            task_name = self.task_var.get()
            TaskClass, module_path = TASK_REGISTRY[task_name]

            # Create the task instance
            self.task = TaskClass(module_path=module_path)

            # Apply UI settings to the task
            if self.task_ui:
                self.task_ui.apply()

            # Start the task
            self.task.start()

            self.running = True
            self.status.config(text=f"Status: Running ({task_name})")
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")

            threading.Thread(target=self.bot_loop, daemon=True).start()

    def stop_bot(self):
        self.running = False

        if self.task:
            self.task.stop()

        self.status.config(text="Status: Stopped")
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

    # ---------------------------------------------------------
    # Main Bot Loop
    # ---------------------------------------------------------
    def bot_loop(self):
        while self.running and self.task.running:
            self.task.loop_all()
            time.sleep(0.05)
