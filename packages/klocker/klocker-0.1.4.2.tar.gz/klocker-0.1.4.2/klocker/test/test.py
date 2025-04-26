import threading
import time
import random

from kmodels.types import Unset, unset

from klocker.simple.locker.config import SimpleLockerConfig
from klocker.simple.locker.locker import SimpleLocker
from klocker.simple.locker.proxy import SimpleLockerProxy
from klocker.simple.thread.state import SimpleThreadLockFailure, SimpleThreadExecutionFailure
from klocker.simple.user import SimpleLockerUserInterface


class Test:
    def __init__(
            self,
            locker: SimpleLocker | Unset = unset,
            n_threads: int = 10,
            worker_duration: float = 2.0,
            worker_sleep_time: float = 0.1,
            exception_rate: int | None = 5,
    ):
        self._locker = SimpleLocker() if isinstance(locker, Unset) else locker
        self._n_threads = n_threads
        self._worker_duration = worker_duration
        self._worker_sleep_time = worker_sleep_time
        self._exception_rate = exception_rate

    def _start_threads(self, worker, *args, **kwargs):
        """Función auxiliar sencilla que inicia los hilos según los settings pasados al constructor."""
        threads = [
            threading.Thread(name=str(i), target=worker, args=args, kwargs=kwargs) for i in range(self._n_threads)
        ]

        for thread in threads:
            thread.start()

        # esperar a que terminen los hilos
        for thread in threads:
            thread.join()

    def _generate_exception_randomly(self):
        if self._exception_rate is None:
            return
        number = random.randint(1, self._exception_rate)
        if number == 1:
            raise ValueError("Sample exception")

    @staticmethod
    def _print_fail_message(ui: SimpleLockerUserInterface):
        t_id = ui.thread.name
        if ui.thread.state.has_failed:
            m = f"\tThread-{t_id} "
            if isinstance(ui.thread.state.failure_details, SimpleThreadLockFailure):
                m += f"failed to enter the locker. "
            elif isinstance(ui.thread.state.failure_details, SimpleThreadExecutionFailure):
                m += f"was interrupted in the middle of it's execution.) "
            else:  # Optional: handle other failure types (if any)
                m += "unknown error. "
            print(m + f"Reason: {repr(ui.thread.state.failure_details)}")

    def _without_with_locker(self, proxy: SimpleLockerProxy):
        """
        Función de ejemplo para usar with directamente. Ya que es inseguro pasar el Locker en su totalidad, pasamos
        un proxy que contiene todas las funcionalidades de enter/exit (incluso stop) amoldadas para no causar problemas.

        Al igual que los otros ejemplos, se puede usar proxy.ui.stop() para detener el locker desde el hilo si es que
        fuera necesario.
        """
        ui = proxy.ui
        t_id = ui.thread.name
        with proxy:
            # Leave if not acquired
            if not ui.thread.state.acquired:
                print(f"Thread-{t_id} failed to enter the locker. Reason: {ui.thread.state.failure_details}")
                return

            # Simulate work in the critical section
            print(f"Thread-{t_id} entered the locker.")

            # Raise sample exception
            try:
                self._generate_exception_randomly()
            except ValueError as e:  # We have to catch the exception by ourselves to not break the thread
                print(f"\t-> Exception caught in the thread: {repr(e)}")
                return False

            return ui.sleep(self._worker_duration, sleep_time=self._worker_sleep_time)

    def _with_locker_everything_in_one(self, ui: SimpleLockerUserInterface):
        """Función de ejemplo para usar con with_locker() que maneja todo en una sola función."""
        t_id = ui.thread.name

        if ui.thread.state.has_failed:
            self._print_fail_message(ui)

        # Simulate work in the critical section
        print(f"Thread-{t_id} entered the locker.")
        self._generate_exception_randomly()
        return ui.sleep(self._worker_duration, sleep_time=self._worker_sleep_time)

    def _with_locker_pair_func(self, ui: SimpleLockerUserInterface):
        """
        Función de ejemplo para usar con with_locker() que se ejecuta si se obtiene el bloqueo.
        Su pareja es with_locker_pair_callback() (aunque puedes no usarlo si no es necesario).
        """
        # Simulate work in the critical section
        t_id = ui.thread.name
        print(f"Thread-{t_id} entered the locker.")
        self._generate_exception_randomly()
        return ui.sleep(self._worker_duration, sleep_time=self._worker_sleep_time)

    def _with_locker_pair_callback(self, ui: SimpleLockerUserInterface):
        self._print_fail_message(ui)

    def using_locker_directly(self):
        """
        Una función que usa with, el cual usa la configuración del locker, pero que no permite configuración para esta
        llamada. Además, es necesario pasar el locker como argumento, para poder usar with por lo que no aisla
        demasiado bien.
        """
        self._start_threads(self._without_with_locker, self._locker.proxy)

    def using_with_locker_everything_in_one(self):
        # everything_in_one executes even if the callback fails
        self._start_threads(
            lambda: self._locker.with_locker(self._with_locker_everything_in_one, 'func'),
        )

    def using_with_locker_pairs(self):
        self._start_threads(
            lambda: self._locker.with_locker(self._with_locker_pair_func, self._with_locker_pair_callback),
        )

    def using_with_locker_without_callback(self):
        self._start_threads(
            lambda: self._locker.with_locker(self._with_locker_pair_func, None),
        )


def test():
    locker = SimpleLocker(
        config=SimpleLockerConfig(on_locked='wait', timeout=None, max_waiters=None, stop_event_delay=0.1)
    )
    testing = Test(locker, n_threads=10, worker_duration=5., worker_sleep_time=0.1, exception_rate=None)
    try:
        # testing.using_locker_directly()
        # testing.using_with_locker_everything_in_one()
        testing.using_with_locker_pairs()
        # testing.using_with_locker_without_callback()
    except KeyboardInterrupt:
        locker.stop()


if __name__ == "__main__":
    test()
