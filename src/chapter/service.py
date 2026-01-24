from src.chapters.models import Chapter
from src.chapters.repository import ChapterRepository
from src.chapters.schemas import ChapterCreate, ChapterUpdate
from src.core.service import AbstractService


class ChapterService(
    AbstractService[Chapter, ChapterCreate, ChapterUpdate, ChapterRepository]
):
    def __init__(self, repository: ChapterRepository) -> None:
        super().__init__(repository)
