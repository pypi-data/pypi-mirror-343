from ctesiphon.dto.base import BaseDTO
from ctesiphon.dbo import RethinkDBBaseDBO
from ctesiphon.repositories import ModelRepository

from ..enums import EmailTypes


class EmailSettingsDTO(BaseDTO):
    type: EmailTypes
    template: str
    subject: str


class EmailSettingsDBO(RethinkDBBaseDBO):
    __tablename__ = "communications__email_settings"
    __indexes__ = [
        "type",
    ]

    type: EmailTypes
    template: str
    subject: str


class EmailSettingsRepository(ModelRepository[EmailSettingsDTO, EmailSettingsDBO]):
    async def get_by_type(self, type: EmailTypes) -> EmailSettingsDTO | None:
        return await self.get_by_params({"type": type})
