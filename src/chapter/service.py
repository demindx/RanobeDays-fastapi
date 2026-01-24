from src.chapter.models import Chapter
from src.chapter.repository import ChapterRepository
from src.chapter.schemas import ChapterCreate, ChapterUpdate
from src.core.service import AbstractService


class ChapterService(
    AbstractService[Chapter, ChapterCreate, ChapterUpdate, ChapterRepository]
):
    def __init__(self, repository: ChapterRepository) -> None:
        super().__init__(repository)
