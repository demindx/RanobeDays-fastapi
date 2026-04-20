from fastapi import APIRouter

from src.category.dependencies import CategoryServiceDep
from src.category.schemas import CategoryCreate, CategoryReponse, CategoryUpdate
from src.config import config
from src.core.schemas import GenericPaginationResponse, GenericResponse

router = APIRouter(prefix="/category", tags=["category"])


@router.get("/")
async def get_categories(
    service: CategoryServiceDep,
    limit: int = config.DEFAULT_PAGINATION_LIMIT,
    offset: int = 0,
) -> GenericPaginationResponse[CategoryReponse]:
    categories = await service.get_all(limit=limit, offset=offset)

    categories = [CategoryReponse.model_validate(category) for category in categories]

    return GenericPaginationResponse[CategoryReponse](
        data=categories, limit=limit, offset=offset
    )


@router.post("/")
async def create_category(
    data: CategoryCreate, service: CategoryServiceDep
) -> GenericResponse[CategoryReponse]:
    category = await service.create(data)

    category = CategoryReponse.model_validate(category)

    return GenericResponse[CategoryReponse](data=category)


@router.get("/{id}")
async def get_category(
    id: int, service: CategoryServiceDep
) -> GenericResponse[CategoryReponse]:
    category = await service.get_by_id(id)

    category = CategoryReponse.model_validate(category)

    return GenericResponse[CategoryReponse](data=category)


@router.patch("/{id}")
async def update_category(
    id: int, data: CategoryUpdate, service: CategoryServiceDep
) -> GenericResponse[CategoryReponse]:
    category = await service.update(id, data)

    category = CategoryReponse.model_validate(category)

    return GenericResponse[CategoryReponse](data=category)


@router.delete("/{id}")
async def delete_category(id: int, service: CategoryServiceDep) -> None:
    await service.delete(id)
