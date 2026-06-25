from fastapi import APIRouter

from src.core.schemas import GenericResponse
from src.novel.dependencies import NovelServiceDep
from src.novel.schemas import NovelCreate, NovelResponse, NovelUpdate

router = APIRouter(prefix="/novel", tags=["novel"])


@router.get("/")
async def get_novels(service: NovelServiceDep) -> GenericResponse[list[NovelResponse]]:
    novels = await service.get_all()

    novels = [NovelResponse.model_validate(novel) for novel in novels]

    return GenericResponse[list[NovelResponse]](data=novels)


@router.get("/{id}")
async def get_novel(
    id: int, service: NovelServiceDep
) -> GenericResponse[NovelResponse]:
    novel = await service.get_by_id(id)

    return GenericResponse[NovelResponse](data=NovelResponse.model_validate(novel))


@router.post("/")
async def create_novel(
    service: NovelServiceDep, data: NovelCreate
) -> GenericResponse[NovelResponse]:
    novel = await service.create(data)

    return GenericResponse[NovelResponse](data=NovelResponse.model_validate(novel))


@router.patch("/{id}")
async def update_novel(
    id: int, data: NovelUpdate, service: NovelServiceDep
) -> GenericResponse[NovelResponse]:
    novel = await service.update(id, data)

    return GenericResponse[NovelResponse](data=NovelResponse.model_validate(novel))


@router.delete("/{id}")
async def delete_novel(id: int, service: NovelServiceDep) -> None:
    await service.delete(id)
