from jinja2 import Environment, FileSystemLoader, select_autoescape

from ..enums import EmailStatuses
from ..interfaces import CtCommunicationsContainer
from ..models import EmailDTO


async def emails_handler(
    container: CtCommunicationsContainer,
    email: EmailDTO,
):
    j2_env = Environment(
        loader=FileSystemLoader(container.settings.communications.email_templates_dir),
        autoescape=select_autoescape()
    )
    email_settings = await container.email_settings_repo.get_by_type(email.type)
    user = await container.users_repo.get_by_id(email.user_id)

    if email_settings and user:
        template = j2_env.get_template(email_settings.template)

        user_email = getattr(user, container.settings.communications.user_email_field)

        email_external_id = await container.send_email(
            receiver=str(user_email),
            sender=container.settings.communications.email_sender,
            subject=email_settings.subject,
            body=template.render(email.params),
        )

        if not email_external_id:
            email.status = EmailStatuses.ERROR
        else:
            email.external_id = email_external_id
            email.status = EmailStatuses.SENDED

        await container.emails_repo.save(email)
