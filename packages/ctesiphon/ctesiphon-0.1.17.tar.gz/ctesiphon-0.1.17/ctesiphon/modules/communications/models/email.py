from ctesiphon.dto.base import BaseDTO
from ctesiphon.dbo import RethinkDBBaseDBO
from ctesiphon.repositories import ModelRepository
from pydantic import UUID4

from ..enums import (
    EmailTypes,
    EmailStatuses,
)


class EmailDTO(BaseDTO):
    user_id: UUID4
    params: dict
    type: EmailTypes
    external_id: str | None = None
    status: EmailStatuses = EmailStatuses.CREATED


class EmailDBO(RethinkDBBaseDBO):
    __tablename__ = "communications__emails"
    __indexes__ = [
        "user_id",
        "type",
        "status",
    ]

    user_id: UUID4
    params: dict
    type: EmailTypes
    external_id: str | None = None
    status: EmailStatuses = EmailStatuses.CREATED


class EmailsRepository(ModelRepository[EmailDTO, EmailDBO]):
    async def get_new_emails(self) -> list[EmailDTO]:
        return await self.get_list_by_params({"status": EmailStatuses.CREATED})
