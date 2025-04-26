from ctesiphon.repositories import ModelRepository

from .settings import CtCommunicationsSettings
from ..models import (
    EmailsRepository,
    EmailSettingsRepository,
)


class CtCommunicationsContainer:
    settings: CtCommunicationsSettings

    emails_repo: EmailsRepository
    email_settings_repo: EmailSettingsRepository
    users_repo: ModelRepository

    def __init__(self):
        from ..helpers import send_email_factory

        self.send_email = send_email_factory(self)
