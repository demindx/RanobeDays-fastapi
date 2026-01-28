from src.core.service import AbstractService
from src.language.models import Language
from src.language.repository import LanguageRepository
from src.language.schemas import LanguageCreate, LanguageUpdate


class LanguageService(
    AbstractService[Language, LanguageCreate, LanguageUpdate, LanguageRepository]
):
    def __init__(self, repository: LanguageRepository) -> None:
        super().__init__(repository)
