import os
import json
import importlib
import inspect

from Tasks.Task import Task

MODULES_PATH = os.path.dirname(__file__)

TASK_REGISTRY = {}        # { "Mining": (TaskClass, module_dir) }
TASK_UI_REGISTRY = {}     # { "Mining": UIClass }
MODULE_INFO = {}          # Raw module.json data


def load_modules():
    """
    Loads all modules inside /Modules/<ModuleName>/
    Expected structure:
        Modules/<ModuleName>/
            module.json
            task.py  -> class Task (subclass of base Task)
            ui.py    -> class TaskUI (optional)
            icon.png (optional)
    """

    for folder in os.listdir(MODULES_PATH):
        module_dir = os.path.join(MODULES_PATH, folder)

        if not os.path.isdir(module_dir):
            continue

        # ---------------------------------------------------------
        # Load module.json
        # ---------------------------------------------------------
        json_path = os.path.join(module_dir, "module.json")
        if not os.path.exists(json_path):
            continue

        try:
            with open(json_path, "r") as f:
                info = json.load(f)
        except Exception as e:
            print(f"[Module Loader] Failed to read module.json in {folder}: {e}")
            continue

        MODULE_INFO[folder] = info
        display_name = info.get("name", folder)

        # ---------------------------------------------------------
        # Load task.py
        # ---------------------------------------------------------
        try:
            task_module = importlib.import_module(f"Modules.{folder}.task")

            TaskClass = None
            for _, obj in inspect.getmembers(task_module, inspect.isclass):
                if issubclass(obj, Task) and obj is not Task:
                    TaskClass = obj
                    break

            if TaskClass is None:
                raise Exception("No Task subclass found")

        except Exception as e:
            print(f"[Module Loader] Failed to load Task for {display_name}: {e}")
            continue

        # ---------------------------------------------------------
        # Load ui.py (optional)
        # ---------------------------------------------------------
        UIClass = None
        ui_path = os.path.join(module_dir, "ui.py")

        if os.path.exists(ui_path):
            try:
                ui_module = importlib.import_module(f"Modules.{folder}.ui")

                # Look for class named TaskUI or <ModuleName>UI
                for _, obj in inspect.getmembers(ui_module, inspect.isclass):
                    if obj.__name__.lower() in (
                        "taskui",
                        f"{folder.lower()}ui",
                        f"{display_name.lower()}ui"
                    ):
                        UIClass = obj
                        break

                if UIClass is None:
                    raise Exception("No UI class found")

            except Exception as e:
                print(f"[Module Loader] Failed to load UI for {display_name}: {e}")

        # ---------------------------------------------------------
        # Register module
        # ---------------------------------------------------------
        TASK_REGISTRY[display_name] = (TaskClass, module_dir)

        if UIClass:
            TASK_UI_REGISTRY[display_name] = UIClass

        print(f"[Module Loader] Loaded module: {display_name}")


# Load modules on import
load_modules()
