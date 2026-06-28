import importlib
import inspect
import json
import os

from Classes.Constants import MODULE_CONFIG_FILENAME
from Tasks.Task import Task

MODULES_PATH = os.path.dirname(__file__)

# Registry of raw module information loaded from configs files
MODULE_INFO = {}
# Registry of loaded Task classes and their associated information
TASK_REGISTRY = {}
# Registry of loaded TaskUI classes and their associated information
TASK_UI_REGISTRY = {}


def load_modules():
    """Loads all modules inside the `Modules` directory and registers their Task and TaskUI classes."""

    for folder in os.listdir(MODULES_PATH):
        module_dir = os.path.join(MODULES_PATH, folder)

        if not os.path.isdir(module_dir):
            continue

        # ---------------------------------------------------------
        # Load json configs
        # ---------------------------------------------------------
        json_path = os.path.join(module_dir, MODULE_CONFIG_FILENAME)
        if not os.path.exists(json_path):
            continue

        try:
            with open(json_path, "r") as f:
                info = json.load(f)
        except Exception as e:
            print(
                f"[Module Loader] Failed to read {MODULE_CONFIG_FILENAME} in {folder}: {e}"
            )
            continue

        MODULE_INFO[folder] = info
        moduleName = info.get("name", folder)
        moduleConfigs = info.get("configs", {})
        moduleIsRunnable = info.get("runnable", False)
        moduleDescription = info.get("description", "")

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
            print(f"[Module Loader] Failed to load Task for {moduleName}: {e}")
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
                        f"{moduleName.lower()}ui",
                    ):
                        UIClass = obj
                        break

                if UIClass is None:
                    raise Exception("No UI class found")

            except Exception as e:
                print(f"[Module Loader] Failed to load UI for {moduleName}: {e}")

        # ---------------------------------------------------------
        # Register module
        # ---------------------------------------------------------
        TASK_REGISTRY[moduleName] = {
            "task": TaskClass,
            "path": module_dir,
            "configs": moduleConfigs,
            "runnable": moduleIsRunnable,
            "description": moduleDescription,
        }

        if UIClass:
            TASK_UI_REGISTRY[moduleName] = UIClass

        print(f"[Module Loader] Loaded module: {moduleName}")


# Load modules on  import
load_modules()
