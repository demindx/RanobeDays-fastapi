from src.novel.repository import NovelRepository


class NovelService:
    def __init__(self, repository: NovelRepository):
        self._repo: NovelRepository = repository
