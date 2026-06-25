from fastapi import APIRouter

from src.chapter.dependencies import ChapterServiceDep
from src.chapter.schemas import ChapterCreate, ChapterResponse, ChapterUpdate
from src.core.schemas import GenericResponse

router = APIRouter(prefix="/chapter", tags=["chapter"])


@router.get("/")
async def get_chapters(
    service: ChapterServiceDep,
) -> GenericResponse[list[ChapterResponse]]:
    """
    Returns list of all chapters
    """
    chapters = await service.get_all()

    chapters = [ChapterResponse.model_validate(chapter) for chapter in chapters]

    return GenericResponse[list[ChapterResponse]](data=chapters)


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
