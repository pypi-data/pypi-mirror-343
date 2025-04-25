from ctesiphon.dto.base import BaseDTO

from ..interfaces import CtCommunicationsContainer
from ..enums import (
    EmailTypes,
    EmailStatuses,
)
from ..models import EmailDTO


def create_email_factory(container: CtCommunicationsContainer):
    async def func(
        user: BaseDTO,
        params: dict,
        type: EmailTypes,
    ) -> EmailDTO:
        return await container.emails_repo.save(EmailDTO(
            user_id=user.id,
            params=params,
            type=type,
            status=EmailStatuses.CREATED,
        ))
    return func
