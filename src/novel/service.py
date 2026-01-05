from src.core.service import AbstractService
from src.novel.models import Novel
from src.novel.repository import NovelRepository
from src.novel.schemas import NovelCreate, NovelUpdate


class NovelService(AbstractService[Novel, NovelCreate, NovelUpdate, NovelRepository]):
    def __init__(self, repository: NovelRepository) -> None:
        super().__init__(repository)
