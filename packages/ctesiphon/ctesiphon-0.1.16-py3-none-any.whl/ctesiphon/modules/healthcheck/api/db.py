from fastapi import Depends

from .router import router
from ..errors import HealthcheckDBError
from ....interfaces.container import CtContainer, get_container


@router.get(
    "/db",
    summary="Эндпоинт возвращает статус системных БД",
    response_model=bool,
)
async def db_healthcheck(
    container: CtContainer = Depends(get_container),
):
    result = False

    try:
        result = await container.rethinkdb_driver.check_db()
    except:
        result = False

    if not result:
        raise HealthcheckDBError

    return result
