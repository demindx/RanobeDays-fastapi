from datetime import UTC, datetime

import httpx
import pytest
from pydantic import BaseModel, ValidationError

from src.category.schemas import CategoryCreate, CategoryUpdate
from src.chapter.schemas import ChapterCreate, ChapterUpdate
from src.country.schemas import CountryCreate, CountryUpdate
from src.language.schemas import LanguageCreate, LanguageUpdate
from src.main import app
from src.novel.schemas import NovelCreate, NovelUpdate
from src.teams.schemas import TeamAddUser, TeamCreate, TeamUpdate
from src.users.schemas import (
    UserLogin,
    UserPasswordUpdate,
    UserProfileUpdate,
    UserRegister,
)

PAGINATED_ENDPOINTS = [
    "/api/v1/users/",
    "/api/v1/teams/",
    "/api/v1/teams/1/novels",
    "/api/v1/novel/",
    "/api/v1/chapter/",
    "/api/v1/category/",
    "/api/v1/lang/",
    "/api/v1/country/",
]


@pytest.mark.parametrize("endpoint", PAGINATED_ENDPOINTS)
@pytest.mark.parametrize(
    "invalid_query",
    [
        "limit=0",
        "limit=101",
        "offset=-1",
    ],
)
@pytest.mark.usefixtures("client")
async def test_pagination_rejects_values_outside_contract(endpoint, invalid_query):
    transport = httpx.ASGITransport(app=app, raise_app_exceptions=False)
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as validation_client:
        response = await validation_client.get(f"{endpoint}?{invalid_query}")

    assert response.status_code == 422


REQUEST_SCHEMA_CASES: list[tuple[type[BaseModel], dict]] = [
    (
        UserLogin,
        {"login": "user1", "password": "password123"},
    ),
    (
        UserRegister,
        {
            "login": "user1",
            "email": "user1@example.com",
            "nickname": "Nick",
            "password1": "password123",
            "password2": "password123",
        },
    ),
    (UserProfileUpdate, {"nickname": "Nick"}),
    (CategoryCreate, {"name": "Fantasy", "type": "genre"}),
    (CategoryUpdate, {"name": "Fantasy"}),
    (
        ChapterCreate,
        {
            "title": "Chapter 1",
            "number": 1,
            "content": "Content",
            "novel_id": 1,
            "team_id": 1,
        },
    ),
    (ChapterUpdate, {"title": "Chapter 1"}),
    (CountryCreate, {"name": "Japan"}),
    (CountryUpdate, {"name": "Japan"}),
    (LanguageCreate, {"name": "Japanese"}),
    (LanguageUpdate, {"name": "Japanese"}),
    (
        NovelCreate,
        {
            "title": "Novel",
            "age_limit": 16,
            "team_id": 1,
            "language_id": 1,
            "country_id": 1,
            "description": "Description",
            "publish_date": datetime.now(UTC),
            "type": "original",
        },
    ),
    (NovelUpdate, {"title": "Novel"}),
    (TeamCreate, {"creator_id": 1, "name": "Team", "type": "translators"}),
    (TeamUpdate, {"name": "Team"}),
    (TeamAddUser, {"user_id": 1, "role": "manager"}),
]


@pytest.mark.parametrize(("schema", "payload"), REQUEST_SCHEMA_CASES)
def test_request_schema_rejects_unknown_field(schema, payload):
    with pytest.raises(ValidationError):
        schema.model_validate({**payload, "unexpected_field": "unexpected"})


def test_password_update_mismatch_is_pydantic_validation_error():
    with pytest.raises(ValidationError):
        UserPasswordUpdate(
            password1="password123",
            password2="different-password",
        )
