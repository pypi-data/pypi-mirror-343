from enum import StrEnum


class EmailStatuses(StrEnum):
    CREATED = "created"
    SENDED = "sended"
    ERROR = "error"
    DELIVERED = "delivered"
    REJECTED = "rejected"
