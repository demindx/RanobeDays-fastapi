from fastapi import APIRouter

from src.config import config
from src.core.schemas import GenericPaginationResponse, GenericResponse
from src.country.dependencies import CountryServiceDep
from src.country.schemas import CountryCreate, CountryResponse, CountryUpdate

router = APIRouter(prefix="/country", tags=["country"])


@router.get("/")
async def get_countries(
    service: CountryServiceDep,
    limit: int = config.DEFAULT_PAGINATION_LIMIT,
    offset: int = 0,
) -> GenericPaginationResponse[CountryResponse]:
    languages = await service.get_all(limit=limit, offset=offset)

    languages = [CountryResponse.model_validate(language) for language in languages]

    return GenericPaginationResponse[CountryResponse](
        data=languages, limit=limit, offset=offset
    )


@router.post("/")
async def create_country(
    data: CountryCreate, service: CountryServiceDep
) -> GenericResponse[CountryResponse]:
    language = await service.create(data)

    language = CountryResponse.model_validate(language)

    return GenericResponse[CountryResponse](data=language)


@router.get("/{id}")
async def get_country(
    id: int, service: CountryServiceDep
) -> GenericResponse[CountryResponse]:
    language = await service.get_by_id(id)

    language = CountryResponse.model_validate(language)

    return GenericResponse[CountryResponse](data=language)


@router.patch("/{id}")
async def update_country(
    id: int, data: CountryUpdate, service: CountryServiceDep
) -> GenericResponse[CountryResponse]:
    language = await service.update(id, data)

    language = CountryResponse.model_validate(language)

    return GenericResponse[CountryResponse](data=language)


@router.delete("/{id}")
async def delete_country(id: int, service: CountryServiceDep) -> None:
    await service.delete(id)
