import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import threading

from Modules.loader import TASK_REGISTRY, TASK_UI_REGISTRY
from Logger import Logger


class Scheduler(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.running = False
        self.task = None
        self.task_ui = None
        self.active_module = None
        self.icons = {}
        self.runnable = True

        # Per-module task + running tracking (one running module at a time)
        self.module_tasks = {}
        self.module_running = {}
        self.currently_running_module = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=0)
        self.rowconfigure(5, weight=1)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Tab.TButton",
            background="#e6e6e6",
            foreground="#111111",
            padding=(14, 6),
            relief="raised",
            borderwidth=1,
        )
        style.map("Tab.TButton", background=[("active", "#dcdcdc")])

        style.configure(
            "TabActive.TButton",
            background="#ffffff",
            foreground="#111111",
            padding=(14, 6),
            relief="flat",
            borderwidth=1,
        )

        style.configure("TFrame", background="#f2f2f2")
        style.configure("TLabelframe", background="#f2f2f2", foreground="#111111")
        style.configure(
            "TLabelframe.Label",
            background="#f2f2f2",
            foreground="#111111",
            font=("Segoe UI", 10, "bold"),
        )
        style.configure("TLabel", background="#f2f2f2", foreground="#111111")

        style.configure("TButton", background="#e6e6e6", foreground="#111111", padding=6)
        style.map("TButton", background=[("active", "#d9d9d9")])

        # Used by Modules/ModuleUI.py
        style.configure("ModulePanel.TFrame", background="#f2f2f2")
        style.configure("ModuleCard.TFrame", background="#ffffff", borderwidth=1, relief="solid")

        # ---------------- TOP BAR ----------------
        topbar = ttk.Frame(self)
        topbar.grid(row=0, column=0, sticky="ew", pady=5, padx=10)
        topbar.columnconfigure(1, weight=1)

        ttk.Label(
            topbar,
            text="RuneScape Automation Tool",
            font=("Segoe UI", 16, "bold"),
        ).grid(row=0, column=1, sticky="n")

        # ---------------- CONSOLE ----------------
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
            state="disabled",
        )
        self.log_text.grid(row=0, column=0, sticky="nsew")

        self.log_text.tag_config("INFO", foreground="#111111")
        self.log_text.tag_config("ACTION", foreground="#007acc")
        self.log_text.tag_config("ERROR", foreground="#cc0000")
        self.log_text.tag_config("SUCCESS", foreground="#008000")
        self.log_text.tag_config("DEBUG", foreground="#b8860b")

        Logger.gui_callback = self.gui_log
        Logger.copy_callback = self.copy_log
        Logger.gui_clear_callback = self.clear_log

        console_buttons = ttk.Frame(self)
        console_buttons.grid(row=2, column=0, sticky="e", padx=10, pady=(0, 5))

        ttk.Button(console_buttons, text="Copy Console", command=Logger.Copy).pack(
            side="right", padx=5
        )
        ttk.Button(console_buttons, text="Clear Console", command=Logger.Clear).pack(
            side="right"
        )

        # ---------------- TABS ----------------
        tab_frame = ttk.Frame(self)
        tab_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(5, 0))

        self.module_buttons = {}
        self.module_ui_instances = {}  # { module_name: UI instance or None }

        for module_name, meta in TASK_REGISTRY.items():
            icon = self.load_icon(meta["path"])
            btn = ttk.Button(
                tab_frame,
                text=f"  {module_name}",
                image=icon,
                compound="left",
                style="Tab.TButton",
                command=lambda m=module_name: self.switch_module(m),
            )
            btn.pack(side="left", padx=(0, 4))
            self.module_buttons[module_name] = btn

        separator = ttk.Separator(self, orient="horizontal")
        separator.grid(row=4, column=0, sticky="ew")

        # ---------------- PANEL CONTAINER ----------------
        self.panel_container = ttk.Frame(self)
        self.panel_container.grid(row=5, column=0, sticky="nsew", padx=10, pady=5)
        self.panel_container.columnconfigure(0, weight=1)
        self.panel_container.rowconfigure(0, weight=1)
        self.panel_container.rowconfigure(1, weight=0)

        self.module_content = {}  # { module_name: module_ui_frame }

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

        self.active_module = module_name

        meta = TASK_REGISTRY[module_name]
        TaskClass = meta["task"]
        module_path = meta["path"]
        self.runnable = meta["runnable"]
        configs = meta["configs"]

        # Create task instance for UI apply/config updates
        self.task = TaskClass(module_path=module_path, configs=configs)

        # UI cache
        if module_name in self.module_ui_instances and self.module_ui_instances[module_name] is not None:
            self.task_ui = self.module_ui_instances[module_name]
            self.task_ui.task = self.task
        else:
            self.task_ui = None

        # Create module frame once
        if module_name not in self.module_content:
            module_ui_frame = ttk.Frame(self.panel_container)
            module_ui_frame.grid(row=0, column=0, sticky="nsew")
            module_ui_frame.columnconfigure(0, weight=1)
            module_ui_frame.rowconfigure(0, weight=1)
            module_ui_frame.grid_propagate(False)
            self.module_content[module_name] = module_ui_frame

            UIClass = TASK_UI_REGISTRY.get(module_name)
            if UIClass:
                self.task_ui = UIClass(module_ui_frame, self.task, configs)
                self.module_ui_instances[module_name] = self.task_ui
                widget = self.task_ui.widget()
                widget.grid(row=0, column=0, sticky="nsew")
            else:
                self.module_ui_instances[module_name] = None

        # Show only selected module frame
        for name, frame in self.module_content.items():
            if name == module_name:
                frame.grid(row=0, column=0, sticky="nsew")
            else:
                frame.grid_remove()

        # Control bar
        if hasattr(self, "control_bar") and self.control_bar.winfo_exists():
            self.control_bar.destroy()

        self.control_bar = ttk.Frame(self.panel_container)
        self.control_bar.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        self.control_bar.columnconfigure(1, weight=1)

        if self.runnable:
            is_running_this = self.module_running.get(module_name, False)
            btn_text = "Stop" if is_running_this else "Start"
            self.toggle_btn = ttk.Button(
                self.control_bar, text=btn_text, command=self.toggle_module
            )
            self.toggle_btn.grid(row=0, column=0, padx=5)

            status_text = (
                f"Status: Running ({module_name})" if is_running_this else "Status: Idle"
            )
            self.status = ttk.Label(self.control_bar, text=status_text)
            self.status.grid(row=0, column=1, sticky="w")
        else:
            self.status = ttk.Label(self.control_bar, text="Status: Settings-only")
            self.status.grid(row=0, column=0, sticky="w", padx=5)


    # ---------------------------------------------------------
    # LOGGING
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # MODULE CONTROL
    # ---------------------------------------------------------
    def toggle_module(self):
        if not self.active_module:
            return

        if self.module_running.get(self.active_module, False):
            self.stop_module(self.active_module)
        else:
            self.start_module(self.active_module)

    def start_module(self, module_name):
        if not self.runnable:
            Logger.Error(f"Module {module_name} cannot be started (settings-only).")
            return

        if self.currently_running_module and self.currently_running_module != module_name:
            Logger.Error(f"Only one module can run at a time. Stop '{self.currently_running_module}' first.")
            return

        if self.module_running.get(module_name, False):
            return

        if module_name not in self.module_tasks:
            meta = TASK_REGISTRY[module_name]
            TaskClass = meta["task"]
            module_path = meta["path"]
            configs = meta["configs"]
            self.module_tasks[module_name] = TaskClass(module_path=module_path, configs=configs)

        task = self.module_tasks[module_name]

        ui = self.module_ui_instances.get(module_name)
        if ui is not None:
            ui.task = task
            ui.apply()

        task.start()
        self.module_running[module_name] = True
        self.running = True
        self.currently_running_module = module_name

        if self.active_module == module_name:
            self.toggle_btn.config(text="Stop")
            self.status.config(text=f"Status: Running ({module_name})")

        threading.Thread(target=self.module_loop, args=(module_name, task), daemon=True).start()

    def stop_module(self, module_name):
        if not self.module_running.get(module_name, False):
            return

        self.module_running[module_name] = False
        self.running = False
        self.currently_running_module = None

        task = self.module_tasks.get(module_name)
        if task:
            task.stop()

        if self.active_module == module_name:
            self.toggle_btn.config(text="Start")
            self.status.config(text="Status: Idle")

    def module_loop(self, module_name, task):
        while self.module_running.get(module_name, False) and task.running:
            task.loop_all()

