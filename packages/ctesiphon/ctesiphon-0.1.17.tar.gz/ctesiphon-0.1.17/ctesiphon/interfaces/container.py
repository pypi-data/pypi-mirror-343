from functools import lru_cache

from ..drivers.data import RethinkDBDBODriver


class CtContainer:
    rethinkdb_driver: RethinkDBDBODriver


@lru_cache
def get_container():
    try:
        from config import settings
        from container import AppContainer

        return AppContainer(settings)
    except:
        pass
