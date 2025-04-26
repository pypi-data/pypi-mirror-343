import threading
import time
import warnings
from abc import abstractmethod
from collections.abc import Callable
from typing import Concatenate, Literal

from kmodels.types import Unset, unset
from klocker.simple.constants import ON_LOCKED_T, LOCK_FAILURE_T, CALLBACK_T, P, R
from klocker.simple.locker.config import SimpleLockerConfigHandler, SimpleLockerConfigController
from klocker.simple.locker.proxy import SimpleLockerProxy
from klocker.simple.user import SimpleLockerUserInterface
from klocker.simple.thread.state import SimpleThreadLockFailure
from klocker.simple.thread.thread import SimpleLocalThreadController, SimpleLocalThreadHandler


class SimpleLockerPrivate:
    __slots__ = ('_lock', '_stop_event', '_thread', '_config', '_ui', '_proxy')

    _lock: threading.Lock
    _stop_event: threading.Event
    _thread: SimpleLocalThreadHandler
    _config: SimpleLockerConfigHandler
    _ui: SimpleLockerUserInterface

    _waiting_lock: threading.Lock
    _n_waiters: int

    _proxy: SimpleLockerProxy

    @abstractmethod
    def is_stopping(self) -> bool:
        ...

    @property
    @abstractmethod
    def ui(self):
        ...

    @property
    @abstractmethod
    def _thread_controller(self) -> SimpleLocalThreadController:
        ...

    @property
    @abstractmethod
    def _config_controller(self) -> SimpleLockerConfigController:
        ...

    """------------------------------------------------------"""

    def _handle_stopping_from_thread(self, wait: bool):
        if not self._thread.is_main_thread():
            if not self.ui.config.allow_stop_from_threads:
                raise ValueError(
                    "stop() can only be called from the main thread unless LockerConfig.allow_stop_from_threads == "
                    "True. This is totally fine but, it's disabled by default to prevent unexpected things."
                )
            if wait and not self._thread.is_main_thread():
                raise ValueError(
                    "stop() have to be called with stop(wait=False, ...) if you are not in the main thread. You "
                    "shouldn't send the locker directly to the threads, instead of that, it's safer to send "
                    "locker.proxy or to use locker.with_locker(...) to call the thread functions with the "
                    "restricted ui."
                )

    def _handle_stop_event_warnings(self) -> None:
        """
        Handles warnings related to the stop event.

        If the locker is in the process of stopping and warnings are enabled, this method
        emits a warning to notify the user that the locker is being used after calling `stop()`.
        """
        if self.is_stopping() and self.ui.config.warnings and self.ui.config.stop_event_warnings:
            warnings.warn(
                "Se ha intentado usar el locker tras usar stop() (usa clear() o desactiva "
                "stop_event_warnings según convenga para evitar este warning una vez sepas que tu código funciona "
                "correctamente).",
                RuntimeWarning
            )

    def _stop_timeout_validator(self, stop_timeout) -> float | None:
        _stop_timeout = stop_timeout if not isinstance(stop_timeout, Unset) else self.ui.config.stop_timeout
        if isinstance(_stop_timeout, float) and _stop_timeout <= 0.0:
            raise ValueError("stop_timeout must be greater than 0.0. Use None to wait indefinitely.")
        return _stop_timeout

    @staticmethod
    def _calculate_remaining_timeout(start_time: float, timeout: float | None) -> float | None:
        """
        Calculates the remaining timeout based on the elapsed time.

        :param start_time: The time when the operation started.
        :param timeout: The total timeout duration.

        :return: The remaining timeout, or `None` if no time is left.
        """

        if timeout is None:
            return None

        elapsed = max(0.0, time.monotonic() - start_time)
        remaining_timeout = timeout - elapsed
        remaining_timeout = remaining_timeout if remaining_timeout > 0.0 else None
        return remaining_timeout

    @staticmethod
    def _handle_failure(
            failure_reason: LOCK_FAILURE_T | None,
            exception: BaseException | Unset
    ) -> SimpleThreadLockFailure | Unset:
        if isinstance(failure_reason, Unset):
            return unset

        result = unset
        if failure_reason is not None:
            result = SimpleThreadLockFailure(reason=failure_reason, exception=exception)

        return result

    def _callback_handler(
            self,
            *args,
            func: Callable[[Concatenate[SimpleLockerUserInterface, P]], R],
            callback: CALLBACK_T | Unset,
            **kwargs,
    ):
        """
        Handles the execution of the callback function when the lock is not acquired.

        :param func: The original function passed to `with_locker`.
        :param callback: The callback function to execute. Can be 'func', a callable, or `None`.
        """
        _callback = self.ui.config.callback if isinstance(callback, Unset) else callback
        if _callback is None:
            return

        elif isinstance(_callback, str) and _callback == 'func':
            func(self.ui, *args, **kwargs)
            return

        elif isinstance(_callback, Callable):
            # Si no obtenemos el bloqueo delegamos a
            _callback(self.ui, *args, **kwargs)
            return
        else:
            raise TypeError('callback must be a Callable, "func" or None.')

    def _enter_leave(
            self,

    ):
        _failure_reason: LOCK_FAILURE_T | None = 'stop_event' if self.is_stopping() else None
        if not _failure_reason:
            _acquired = self._lock.acquire(blocking=False)
            if not _acquired:
                _failure_reason = 'leave'

        return _failure_reason

    def _enter_wait(self, *, timeout: float | None, max_waiters: int | None):
        _failure_reason: LOCK_FAILURE_T | None = None
        _waited, _acquired, _remaining_timeout = False, False, timeout
        _acquired = False
        _start_time = None

        _acquired = self._lock.acquire(blocking=False)
        # Check if max_waiters is reached (if it's setted up and this only happens the first time)
        if not _acquired and max_waiters is not None:
            _waited = True
            with self._waiting_lock:
                # * Check if the maximum number of waiters has been reached
                if self._n_waiters >= max_waiters:
                    _failure_reason = 'max_waiters'
                    return _failure_reason, _waited  # **

                # * Increment the number of actual waiters
                self._n_waiters += 1

        while not _acquired:
            # Check if the locker is stopping
            if self.is_stopping():
                _failure_reason = 'stop_event'
                break

            # Check if timeout is reached (we don't check it the first time or never if the timeout is None)
            if _start_time is not None:
                _remaining_timeout = self._calculate_remaining_timeout(_start_time, timeout)
                if _remaining_timeout is None:
                    _failure_reason = 'timeout'
                    break

            # Logica de espera segura
            if not _acquired:
                # Si no hemos podido adquirir el lock hacemos una espera segura para ir haciendo las comprobaciones
                _safe_timeout = (
                    self.ui.config.stop_event_delay
                    if _remaining_timeout is None
                    else min(self.ui.config.stop_event_delay, _remaining_timeout)
                )

                # Esperamos lo máximo posible antes de iniciar start_time la primera vez (si es que timeout no es None)
                if timeout is not None and _start_time is None:
                    _start_time = time.monotonic()

                # Esperamos el tiempo seguro (que a diferencia de timeout es muy pequeño para hacer validaciones sin
                # pero lo suficientemente largo para no sobrecargar el sistema)
                _acquired = self._lock.acquire(timeout=_safe_timeout)

        # Decrementamos el número de waiters al terminar de esperar
        if _waited and max_waiters is not None:  # _waited es True si antes lo incrementamos
            with self._waiting_lock:
                self._n_waiters -= 1

        # Si se ha producido algún error pero hemos adquirido el lock, lo liberamos
        if _acquired and _failure_reason is not None:
            _acquired = False
            self._lock.release()

        # Retornamos el resultado, el fallo o no y si hemos esperado
        return _failure_reason, _waited
