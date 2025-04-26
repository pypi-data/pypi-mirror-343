from aiokafka import ConsumerRecord

from ..interfaces import CtCommunicationsContainer
from ..models import EmailDTO

from .emails import emails_handler


async def handle_route(
    container: CtCommunicationsContainer,
    message: ConsumerRecord,
):
    if message.topic == container.settings.communications.email_actions_topic:
        email = EmailDTO.model_validate_json(message.value)

        await emails_handler(container, email)
