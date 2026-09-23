from fastapi import APIRouter

from src.category.dependencies import CategoryServiceDep
from src.category.schemas import CategoryCreate, CategoryResponse, CategoryUpdate
from src.core.dependencies import PaginationDep
from src.core.schemas import GenericPaginationResponse, GenericResponse

router = APIRouter(prefix="/category", tags=["category"])


@router.get("/")
async def get_categories(
    service: CategoryServiceDep, pagination: PaginationDep
) -> GenericPaginationResponse[CategoryResponse]:
    categories = await service.get_all(pagination)

    categories = [CategoryResponse.model_validate(category) for category in categories]

    return GenericPaginationResponse[CategoryResponse](
        data=categories, limit=pagination.limit, offset=pagination.offset
    )


@router.post("/")
async def create_category(
    data: CategoryCreate, service: CategoryServiceDep
) -> GenericResponse[CategoryResponse]:
    category = await service.create(data)

    category = CategoryResponse.model_validate(category)

    return GenericResponse[CategoryResponse](data=category)


@router.get("/{id}")
async def get_category(
    id: int, service: CategoryServiceDep
) -> GenericResponse[CategoryResponse]:
    category = await service.get_by_id(id)

    category = CategoryResponse.model_validate(category)

    return GenericResponse[CategoryResponse](data=category)


@router.patch("/{id}")
async def update_category(
    id: int, data: CategoryUpdate, service: CategoryServiceDep
) -> GenericResponse[CategoryResponse]:
    category = await service.update(id, data)

    category = CategoryResponse.model_validate(category)

    return GenericResponse[CategoryResponse](data=category)


@router.delete("/{id}")
async def delete_category(id: int, service: CategoryServiceDep) -> None:
    await service.delete(id)
