from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Literal, Optional

ActionType = Literal["mouse", "keyboard", "delay"]


@dataclass
class Action:
    active: bool = False
    name: str = "UnknownAction"
    type: ActionType = "delay"

    key: Optional[str] = None
    delay: Optional[float] = None

    x: Optional[int] = None
    y: Optional[int] = None
    speed: Optional[float] = None

    lastExec: Optional[float] = None
    nextExec: Optional[float] = None

    # raw config dict passed at construction
    raw: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        d = self.raw

        self.name = d.get("name", self.name)
        self.type = d.get("type", self.type)

        self.key = d.get("key", self.key)
        self.delay = d.get("delay", self.delay)
        self.active = d.get("active", self.active)

        self.x = d.get("x", self.x)
        self.y = d.get("y", self.y)
        self.speed = d.get("speed", self.speed)

        self.lastExec = d.get("lastExec", self.lastExec)
        self.nextExec = d.get("nextExec", self.nextExec)

    def to_dict(self):
        return {
            "active": self.active,
            "name": self.name,
            "type": self.type,
            "key": self.key,
            "delay": self.delay,
            "speed": self.speed,
            "x": self.x,
            "y": self.y,
            "lastExec": self.lastExec,
            "nextExec": self.nextExec,
        }
