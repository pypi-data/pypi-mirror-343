from ctesiphon.dto.base import BaseError


class HealthcheckDBError(BaseError):
    http_status = 400
    error_code = "HEALTHCHECK_DB_ERROR"
    description = "Хранилище данных не инициализировано"
