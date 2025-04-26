import threading


class SimpleBaseThreadHandler:
    def __init__(self, local_env: threading.local, varname: str):
        self._local_env: threading.local = local_env
        self._varname: str = varname

    def is_initialized(self) -> bool:
        return hasattr(self._local_env, self._varname)


class SimpleBaseLocalThreadDataInterface(SimpleBaseThreadHandler):
    ...


class SimpleBaseLocalThreadDataController(SimpleBaseThreadHandler):
    ...


class SimpleBaseLocalThreadDataGrouper(SimpleBaseThreadHandler):
    ...
