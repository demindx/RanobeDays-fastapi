from fastapi import APIRouter

from src.config import config
from src.core.schemas import GenericPaginationResponse, GenericResponse
from src.language.dependencies import LanguageServiceDep
from src.language.schemas import LanguageCreate, LanguageResponse, LanguageUpdate

router = APIRouter(prefix="/lang", tags=["language"])


@router.get("/")
async def get_languages(
    service: LanguageServiceDep,
    limit: int = config.DEFAULT_PAGINATION_LIMIT,
    offset: int = 0,
) -> GenericPaginationResponse[LanguageResponse]:
    languages = await service.get_all(limit=limit, offset=offset)

    languages = [LanguageResponse.model_validate(language) for language in languages]

    return GenericPaginationResponse[LanguageResponse](
        data=languages, limit=limit, offset=offset
    )


@router.post("/")
async def create_language(
    data: LanguageCreate, service: LanguageServiceDep
) -> GenericResponse[LanguageResponse]:
    language = await service.create(data)

    language = LanguageResponse.model_validate(language)

    return GenericResponse[LanguageResponse](data=language)


@router.get("/{id}")
async def get_language(
    id: int, service: LanguageServiceDep
) -> GenericResponse[LanguageResponse]:
    language = await service.get_by_id(id)

    language = LanguageResponse.model_validate(language)

    return GenericResponse[LanguageResponse](data=language)


@router.patch("/{id}")
async def update_language(
    id: int, data: LanguageUpdate, service: LanguageServiceDep
) -> GenericResponse[LanguageResponse]:
    language = await service.update(id, data)

    language = LanguageResponse.model_validate(language)

    return GenericResponse[LanguageResponse](data=language)


@router.delete("/{id}")
async def delete_language(id: int, service: LanguageServiceDep) -> None:
    await service.delete(id)
