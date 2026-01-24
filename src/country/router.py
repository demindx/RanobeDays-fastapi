from fastapi import APIRouter

from src.core.schemas import GenericResponse
from src.country.dependencies import CountryServiceDep
from src.country.schemas import CountryCreate, CountryResponse, CountryUpdate

router = APIRouter(prefix="/country", tags=["country"])


@router.get("/")
async def get_languages(
    service: CountryServiceDep,
) -> GenericResponse[list[CountryResponse]]:
    languages = await service.get_all()

    languages = [CountryResponse.model_validate(language) for language in languages]

    return GenericResponse[list[CountryResponse]](data=languages)


@router.post("/")
async def create_language(
    data: CountryCreate, service: CountryServiceDep
) -> GenericResponse[CountryResponse]:
    language = await service.create(data)

    language = CountryResponse.model_validate(language)

    return GenericResponse[CountryResponse](data=language)


@router.get("/{id}")
async def get_language(
    id: int, service: CountryServiceDep
) -> GenericResponse[CountryResponse]:
    language = await service.get_by_id(id)

    language = CountryResponse.model_validate(language)

    return GenericResponse[CountryResponse](data=language)


@router.patch("/{id}")
async def update_language(
    id: int, data: CountryUpdate, service: CountryServiceDep
) -> GenericResponse[CountryResponse]:
    language = await service.update(id, data)

    language = CountryResponse.model_validate(language)

    return GenericResponse[CountryResponse](data=language)


@router.delete("/{id}")
async def delete_language(id: int, service: CountryServiceDep) -> None:
    await service.delete(id)
