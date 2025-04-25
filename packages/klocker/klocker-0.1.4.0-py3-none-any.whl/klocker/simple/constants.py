from __future__ import annotations
from typing import Literal, ParamSpec, TypeVar, Callable

P = ParamSpec("P")
R = TypeVar("R")
ON_LOCKED_T = Literal['wait', 'leave']
LOCK_FAILURE_T = Literal['leave', 'timeout', 'max_waiters', 'stop_event', 'exception']
THREAD_FAILURE_T = Literal['exception']
CALLBACK_T = Literal['func'] | Callable[["SimpleLockerUserInterface", P], R] | None
