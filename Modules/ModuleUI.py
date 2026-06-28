import tkinter as tk
from abc import abstractmethod
from dataclasses import dataclass, field
from tkinter import ttk
from typing import Dict, List

from Classes.Actions import Action
from Services.ActionFactory import ActionFactory
from Tasks.Task import Task


@dataclass
class ModuleUI:
    """Base UI container for a module."""

    task: Task
    parent: tk.Widget
    info: Dict = field(init=False)
    configs: Dict = field(init=False)
    settings: Dict = field(init=False)
    actions: List[Action] = field(init=False)
    subtasks: List[Task] = field(init=False)

    def __init__(self, parent, task):
        self.task = task
        self.parent = parent
        self.info = task.info
        self.configs = task.configs
        self.actions = task.actions
        self.settings = task.settings
        self.subtasks = task.subtasks

        # ---- Outer canvas + scrollbar (for module scrolling) ----
        self._container = ttk.Frame(parent, style="ModulePanel.TFrame")
        self._container.grid(row=0, column=0, sticky="nsew")
        self._container.columnconfigure(0, weight=1)
        self._container.rowconfigure(0, weight=1)

        self._canvas = tk.Canvas(
            self._container,
            background="#f2f2f2",
            highlightthickness=0,
            borderwidth=0,
            bd=0,
        )
        self._canvas.grid(row=0, column=0, sticky="nsew")

        # Keep scrollable content but hide the scrollbar (views can still scroll via mouse wheel)
        v_scroll = ttk.Scrollbar(
            self._container, orient="vertical", command=self._canvas.yview
        )
        v_scroll.grid_forget()
        self._canvas.configure(yscrollcommand=v_scroll.set)

        # Mouse wheel scrolling support for the inner canvas
        def _on_mousewheel(event):
            # Windows: event.delta is typically a multiple of 120
            self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # Important: bind/unbind on enter/leave so only the active tab's
        # module is scrollable.
        self._canvas.bind(
            "<Enter>", lambda e: self._canvas.bind_all("<MouseWheel>", _on_mousewheel)
        )
        self._canvas.bind("<Leave>", lambda e: self._canvas.unbind_all("<MouseWheel>"))

        # Inner frame that holds actual module widgets
        self.frame = ttk.Frame(self._canvas, style="ModuleCard.TFrame")
        # Allow inner widgets to size naturally inside the canvas window.
        # (If we force grid_propagate(False), the embedded frame can collapse.)
        self.frame.grid_propagate(True)

        # Make sure grid-based module UIs can expand vertically.
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self._window_id = self._canvas.create_window(
            (0, 0), window=self.frame, anchor="nw"
        )

        # Keep scroll region updated as the frame size changes
        def _on_frame_configure(_event=None):
            bbox = self._canvas.bbox(self._window_id)
            if bbox is None:
                return
            # bbox = (x1, y1, x2, y2)
            self._canvas.configure(scrollregion=bbox)

        self.frame.bind("<Configure>", _on_frame_configure)

        # Resize canvas window content width to match canvas width
        # Also kick scrollregion update on resize.
        def _on_canvas_configure(event):
            canvas_width = event.width
            self._canvas.itemconfig(self._window_id, width=canvas_width)
            _on_frame_configure()

        self._canvas.bind("<Configure>", _on_canvas_configure)

    @property
    def container(self):
        """Return the outer container frame that holds the canvas and scrollbar."""
        return self._container

    @abstractmethod
    def updateTask(self):
        """Apply the current UI settings to the module's task."""
        pass
