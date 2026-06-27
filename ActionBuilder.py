from __future__ import annotations

from typing import Any, Iterable

from BasicActions import BasicAction


def build_basic_actions(actions: Iterable[dict[str, Any]]) -> list[BasicAction]:
    """Create `BasicAction` instances from module.json `actions` entries."""
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


