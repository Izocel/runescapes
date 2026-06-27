import os
import json
import importlib
import inspect

from Tasks.Task import Task


MODULES_PATH = os.path.dirname(__file__)

TASK_REGISTRY = {}
TASK_UI_REGISTRY = {}
MODULE_INFO = {}


def load_modules():
    for module_name in os.listdir(MODULES_PATH):
        module_dir = os.path.join(MODULES_PATH, module_name)

        if not os.path.isdir(module_dir):
            continue

        json_path = os.path.join(module_dir, "module.json")
        if not os.path.exists(json_path):
            continue

        # Load metadata
        with open(json_path, "r") as f:
            info = json.load(f)

        MODULE_INFO[module_name] = info

        # -----------------------------
        # Load task.py
        # -----------------------------
        try:
            task_module = importlib.import_module(f"Modules.{module_name}.task")

            TaskClass = None
            for _, obj in inspect.getmembers(task_module, inspect.isclass):
                if issubclass(obj, Task) and obj is not Task:
                    TaskClass = obj
                    break

            if TaskClass is None:
                raise Exception(f"No Task subclass found in {module_name}/task.py")

        except Exception as e:
            print(f"[Module Loader] Failed to load task for {module_name}: {e}")
            continue

        # -----------------------------
        # Load ui.py
        # -----------------------------
        try:
            ui_module = importlib.import_module(f"Modules.{module_name}.ui")

            UIClass = None
            for _, obj in inspect.getmembers(ui_module, inspect.isclass):
                if obj.__name__.lower().startswith(module_name.lower()):
                    UIClass = obj
                    break

            if UIClass is None:
                raise Exception(f"No UI class found in {module_name}/ui.py")

        except Exception as e:
            print(f"[Module Loader] Failed to load UI for {module_name}: {e}")
            continue

        # -----------------------------
        # Register module
        # -----------------------------
        display_name = info.get("name", module_name)
        
        TASK_REGISTRY[display_name] = (TaskClass, module_dir)
        TASK_UI_REGISTRY[display_name] = UIClass


# Load modules on import
load_modules()
