from __future__ import annotations

from typing import Any, Iterable

from Classes.BasicActions import BasicAction
from Services.Engine import Engine


class ActionFactory:
    """Factory for creating and managing BasicAction instances."""

    @staticmethod
    def Create(actions: Iterable[dict[str, Any]]) -> list[BasicAction]:
        """Create `BasicAction` instances from plain `actions` entries."""
        basic: list[BasicAction] = []

        for a in actions:
            if a is None:
                continue

            # Allow callers to already pass BasicAction instances.
            if isinstance(a, BasicAction):
                basic.append(a)
                continue

            # Minimal schema requirements.
            name = a.get("name")
            a_type = a.get("type")
            if not name or not a_type:
                continue

            # Keep the builder minimal: only decide `active` default.
            active = a.get("active", True)

            basic.append(
                BasicAction(
                    name=name,
                    type=a_type,
                    key=a.get("key"),
                    delay=a.get("delay"),
                    active=active,
                    x=a.get("x"),
                    y=a.get("y"),
                    speed=a.get("speed"),
                    lastExec=a.get("lastExec"),
                    nextExec=a.get("nextExec"),
                )
            )

        return basic

    @staticmethod
    def ShouldRunActionPayload(action: BasicAction) -> bool:
        """Determine if an action should be executed based on its active state and timing."""
        if not action.active:
            return False

        now = Engine.CurrentTimeStamp()
        if action.nextExec is None or now >= action.nextExec:
            return True

        return False

    @staticmethod
    def UpdateAction(action) -> None:
        """Update action.lastExec / action.nextExec after a successful execution."""
        delay = action.delay
        now = Engine.CurrentTimeStamp()
        action.lastExec = now

        if delay is not None and delay != "":
            try:
                action.nextExec = now + float(delay)
            except Exception:
                action.nextExec = None
        else:
            # keep existing value (or None)
            action.nextExec = action.nextExec

    @staticmethod
    def RunAction(action) -> None:
        """Execute an Action (segmented into gating, execution, timestamp update)."""
        if not ActionFactory.ShouldRunActionPayload(action):
            return

        did_execute = Engine.ExecuteAction(action)
        if did_execute:
            ActionFactory.UpdateAction(action)

    @staticmethod
    def FindByName(actions: Iterable[BasicAction], name: str) -> BasicAction | None:
        """Find a `BasicAction` by name."""
        for action in actions:
            if action.name == name:
                return action
        return None
