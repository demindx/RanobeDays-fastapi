from fastapi import APIRouter

from src.core.schemas import GenericResponse
from src.language.dependencies import LanguageServiceDep
from src.language.schemas import LanguageCreate, LanguageReponse, LanguageUpdate

router = APIRouter(prefix="/lang", tags=["language"])


@router.get("/")
async def get_languages(
    service: LanguageServiceDep,
) -> GenericResponse[list[LanguageReponse]]:
    languages = await service.get_all()

    languages = [LanguageReponse.model_validate(language) for language in languages]

    return GenericResponse[list[LanguageReponse]](data=languages)


@router.post("/")
async def create_language(
    data: LanguageCreate, service: LanguageServiceDep
) -> GenericResponse[LanguageReponse]:
    language = await service.create(data)

    language = LanguageReponse.model_validate(language)

    return GenericResponse[LanguageReponse](data=language)


@router.get("/{id}")
async def get_language(
    id: int, service: LanguageServiceDep
) -> GenericResponse[LanguageReponse]:
    language = await service.get_by_id(id)

    language = LanguageReponse.model_validate(language)

    return GenericResponse[LanguageReponse](data=language)


@router.patch("/{id}")
async def update_language(
    id: int, data: LanguageUpdate, service: LanguageServiceDep
) -> GenericResponse[LanguageReponse]:
    language = await service.update(id, data)

    language = LanguageReponse.model_validate(language)

    return GenericResponse[LanguageReponse](data=language)


@router.delete("/{id}")
async def delete_language(id: int, service: LanguageServiceDep) -> None:
    await service.delete(id)
