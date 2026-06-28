from __future__ import annotations

from typing import Any, Iterable

from Classes.Actions import Action


class ActionFactory:
    """Factory for creating and managing Action instances."""

    @staticmethod
    def Create(actions: Iterable[dict[str, Any]]) -> list[Action]:
        """Create `Action` instances from plain `actions` entries."""
        basic: list[Action] = []

        for a in actions:
            if a is None:
                continue

            # Allow callers to already pass Action instances.
            if isinstance(a, Action):
                basic.append(a)
                continue

            # Create an Action instance from the dictionary.
            basic.append(Action(raw=a))

        return basic

    @staticmethod
    def FindByName(actions: Iterable[Action], name: str) -> Action | None:
        """Find a `Action` by name."""
        for action in actions:
            if action.name == name:
                return action
        return None
