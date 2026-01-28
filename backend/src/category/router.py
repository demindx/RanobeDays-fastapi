from fastapi import APIRouter

from src.category.dependencies import CategoryServiceDep
from src.category.schemas import CategoryCreate, CategoryReponse, CategoryUpdate
from src.core.schemas import GenericResponse

router = APIRouter(prefix="/category", tags=["category"])


@router.get("/")
async def get_categories(
    service: CategoryServiceDep,
) -> GenericResponse[list[CategoryReponse]]:
    categories = await service.get_all()

    categories = [CategoryReponse.model_validate(category) for category in categories]

    return GenericResponse[list[CategoryReponse]](data=categories)


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
