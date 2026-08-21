from fastapi import APIRouter

from src.chapter.dependencies import ChapterServiceDep
from src.chapter.schemas import ChapterCreate, ChapterResponse, ChapterUpdate
from src.config import config
from src.core.schemas import GenericPaginationResponse, GenericResponse

router = APIRouter(prefix="/chapter", tags=["chapter"])


@router.get("/")
async def get_chapters(
    service: ChapterServiceDep,
    limit: int = config.DEFAULT_PAGINATION_LIMIT,
    offset: int = 0,
) -> GenericPaginationResponse[ChapterResponse]:
    """
    Returns list of all chapters
    """
    chapters = await service.get_all(limit=limit, offset=offset)

    chapters = [ChapterResponse.model_validate(chapter) for chapter in chapters]

    return GenericPaginationResponse[ChapterResponse](
        data=chapters, limit=limit, offset=offset
    )


@router.post("/")
async def create_chapter(
    data: ChapterCreate,
    service: ChapterServiceDep,
) -> GenericResponse[ChapterResponse]:
    """
    Creating chapter
    """
    chapter = await service.create(data)

    chapter = ChapterResponse.model_validate(chapter)

    return GenericResponse[ChapterResponse](data=chapter)


@router.get("/{id}")
async def get_chapter(
    id: int, service: ChapterServiceDep
) -> GenericResponse[ChapterResponse]:
    """Get chapter by id"""
    chapter = await service.get_by_id(id)

    chapter = ChapterResponse.model_validate(chapter)

    return GenericResponse[ChapterResponse](data=chapter)


@router.patch("/{id}")
async def update_chapter(
    id: int, data: ChapterUpdate, service: ChapterServiceDep
) -> GenericResponse[ChapterResponse]:
    """Updates chapter"""
    chapter = await service.update(id, data)

    chapter = ChapterResponse.model_validate(chapter)

    return GenericResponse[ChapterResponse](data=chapter)


@router.delete("/{id}")
async def delete_chapter(id: int, service: ChapterServiceDep):
    """
    Deleting chapter
    """

    await service.delete(id)

# TODO: make get all novel chapters
