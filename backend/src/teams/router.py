from fastapi import APIRouter

from src.core.schemas import GenericResponse
from src.novel.schemas import NovelResponse
from src.teams.dependencies import TeamServiceDep
from src.teams.schemas import TeamAddUser, TeamCreate, TeamResponse, TeamUpdate
from src.users.schemas import UserTeamResponse

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post("/")
async def create_team_handler(
    service: TeamServiceDep, data: TeamCreate
) -> GenericResponse[TeamResponse]:
    team = await service.create(data)

    team = TeamResponse.model_validate(team)

    return GenericResponse[TeamResponse](data=team)


@router.get("/")
async def get_teams_handler(
    service: TeamServiceDep,
) -> GenericResponse[list[TeamResponse]]:
    teams = await service.get_all()

    teams = [TeamResponse.model_validate(team) for team in teams]

    return GenericResponse[list[TeamResponse]](data=teams)


@router.get("/{id}")
async def get_team(service: TeamServiceDep, id: int) -> GenericResponse[TeamResponse]:
    team = await service.get_by_id(id)

    team = TeamResponse.model_validate(team)

    return GenericResponse[TeamResponse](data=team)


@router.patch("/{id}")
async def update_team_handler(
    service: TeamServiceDep, data: TeamUpdate, id: int
) -> GenericResponse[TeamResponse]:
    team = await service.update(id, data)

    team = TeamResponse.model_validate(team)

    return GenericResponse[TeamResponse](data=team)


@router.delete("/{id}")
async def delete_team_handler(service: TeamServiceDep, id: int) -> None:
    await service.delete(id)


@router.get("/{id}/users")
async def get_team_users(
    service: TeamServiceDep, id: int
) -> GenericResponse[list[UserTeamResponse]]:
    users = await service.get_users(id)

    users = [UserTeamResponse.from_tuple(user) for user in users]

    return GenericResponse[list[UserTeamResponse]](data=users)


@router.patch("/{id}/users")
async def add_user_to_team_handler(
    service: TeamServiceDep, id: int, data: TeamAddUser
) -> GenericResponse[None]:
    await service.add_user(id, data)

    return GenericResponse[None]()


@router.delete("/{id}/users/{user_id}")
async def remove_user_from_team(service: TeamServiceDep, id: int, user_id: int):
    await service.remove_user(id, user_id)

    return GenericResponse[None]()


@router.get("/{id}/novels")
async def get_novels(
    service: TeamServiceDep, id: int
) -> GenericResponse[list[NovelResponse]]:
    novels = await service.get_novels(id)

    novels = [NovelResponse.model_validate(novel) for novel in novels]

    return GenericResponse[list[NovelResponse]](data=novels)
