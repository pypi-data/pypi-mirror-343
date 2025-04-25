import threading

from kmodels.types import Unset, unset

from klocker.simple.constants import ON_LOCKED_T
from klocker.simple.shared import SimpleBaseLockerThreadConfig
from klocker.simple.thread.base import SimpleBaseLocalThreadDataInterface, SimpleBaseLocalThreadDataController


class SimpleLocalThreadConfig(SimpleBaseLockerThreadConfig):
    """
    Hereda valores como on_locked y timeout de BaseLockerThreadConfig.
    """
    ...


class SimpleLocalThreadConfigInterface(SimpleBaseLocalThreadDataInterface):
    """
    Clase que contiene la configuración del hilo local. Está pensada para ser accedida directamente por el usuario.
    """

    def __init__(self, local_env: threading.local):
        super().__init__(local_env, 'config')

    @property
    def data(self) -> SimpleLocalThreadConfig:
        self._raise_not_initialized()
        return self._local_env.config

    @property
    def on_locked(self) -> ON_LOCKED_T:
        return self.data.on_locked

    @property
    def timeout(self) -> float | None:
        return self.data.timeout

    @property
    def max_waiters(self) -> int | None:
        return self.data.max_waiters


class SimpleLocalThreadConfigController(SimpleBaseLocalThreadDataController):
    """
    Clase que controla la configuración del hilo local. No debe ser pasada al usuario, se puede considerar que es
    un helper para inicializar la configuración del hilo local, entre otros.
    """

    def __init__(self, local_env: threading.local):
        super().__init__(local_env, 'config')

    def initialize(
            self,
            *,
            on_locked: ON_LOCKED_T,
            timeout: float | None,
            max_waiters: int | None
    ):
        self._raise_already_initialized()
        self._local_env.config = SimpleLocalThreadConfig(
            on_locked=on_locked,
            timeout=timeout,
            max_waiters=max_waiters
        )

    def initialize_from_config(self, config: SimpleLocalThreadConfig):
        self.initialize(
            on_locked=config.on_locked,
            timeout=config.timeout,
            max_waiters=config.max_waiters
        )

    def get(self) -> SimpleLocalThreadConfig:
        return self._local_env.config

    def update(
            self,
            *,
            on_locked: ON_LOCKED_T | Unset = unset,
            timeout: float | None | Unset = unset,
            max_waiters: int | None | Unset = unset,
    ):
        _on_locked = on_locked if not isinstance(on_locked, Unset) else self._local_env.config.on_locked
        _timeout = timeout if not isinstance(timeout, Unset) else self._local_env.config.timeout
        _max_waiters = max_waiters if not isinstance(max_waiters, Unset) else self._local_env.config.max_waiters

        config = SimpleLocalThreadConfig(on_locked=_on_locked, timeout=_timeout, max_waiters=_max_waiters)
        self.update_from_config(config)

    def update_from_config(self, config: SimpleLocalThreadConfig):
        self._local_env.config = config
