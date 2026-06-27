from __future__ import annotations

from typing import Any, Literal, Optional

ActionType = Literal["mouse", "keyboard"]


class BasicAction:
    """Structured action object.

    Converted from a dataclass to a regular class to support explicit getter/setter
    semantics while preserving the existing field names used throughout the codebase.
    """

    def __init__(
        self,
        name: str,
        type: ActionType,
        key: Optional[str] = None,
        delay: Optional[float] = None,
        active: bool = True,
        x: Optional[int] = None,
        y: Optional[int] = None,
        speed: Optional[float] = None,
        lastExec: Optional[float] = None,
        nextExec: Optional[float] = None,
    ):
        self._name = name
        self._type = type
        self._key = key
        self._delay = delay
        self._active = active

        self._x = x
        self._y = y
        self._speed = speed

        self._lastExec = lastExec
        self._nextExec = nextExec

    # -------------------- core fields --------------------
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def type(self) -> ActionType:
        return self._type

    @type.setter
    def type(self, value: ActionType) -> None:
        self._type = value

    @property
    def key(self) -> Optional[str]:
        return self._key

    @key.setter
    def key(self, value: Optional[str]) -> None:
        self._key = value

    @property
    def delay(self) -> Optional[float]:
        return self._delay

    @delay.setter
    def delay(self, value: Optional[float]) -> None:
        self._delay = value

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        self._active = value

    # -------------------- mouse params --------------------
    @property
    def x(self) -> Optional[int]:
        return self._x

    @x.setter
    def x(self, value: Optional[int]) -> None:
        self._x = value

    @property
    def y(self) -> Optional[int]:
        return self._y

    @y.setter
    def y(self, value: Optional[int]) -> None:
        self._y = value

    @property
    def speed(self) -> Optional[float]:
        return self._speed

    @speed.setter
    def speed(self, value: Optional[float]) -> None:
        self._speed = value

    # -------------------- runtime lifecycle --------------------
    @property
    def lastExec(self) -> Optional[float]:
        return self._lastExec

    @lastExec.setter
    def lastExec(self, value: Optional[float]) -> None:
        self._lastExec = value

    @property
    def nextExec(self) -> Optional[float]:
        return self._nextExec

    @nextExec.setter
    def nextExec(self, value: Optional[float]) -> None:
        self._nextExec = value

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type,
            "key": self.key,
            "delay": self.delay,
            "active": self.active,
            "x": self.x,
            "y": self.y,
            "speed": self.speed,
            "lastExec": self.lastExec,
            "nextExec": self.nextExec,
        }


