import pytest
from pydantic import TypeAdapter, ValidationError

from src.bookmark.schemas import BookmarkName
from src.chapter.schemas import ChapterTitle
from src.country.schemas import CountryName
from src.language.schemas import LanguageName
from src.novel.schemas import CoverPath, NovelSlug, NovelTitle
from src.teams.schemas import TeamName
from src.users.schemas import Login, UserEmail


@pytest.mark.parametrize(
    ("string_type", "max_length"),
    [
        (Login, 50),
        (CountryName, 100),
        (LanguageName, 100),
        (ChapterTitle, 100),
        (BookmarkName, 150),
        (NovelTitle, 255),
        (NovelSlug, 255),
        (CoverPath, 255),
        (TeamName, 255),
    ],
)
def test_string_type_accepts_database_length_limit(string_type, max_length):
    value = "a" * max_length

    assert TypeAdapter(string_type).validate_python(value) == value


@pytest.mark.parametrize(
    ("string_type", "max_length"),
    [
        (Login, 50),
        (CountryName, 100),
        (LanguageName, 100),
        (ChapterTitle, 100),
        (BookmarkName, 150),
        (NovelTitle, 255),
        (NovelSlug, 255),
        (CoverPath, 255),
        (TeamName, 255),
    ],
)
def test_string_type_rejects_value_over_database_limit(string_type, max_length):
    with pytest.raises(ValidationError):
        TypeAdapter(string_type).validate_python("a" * (max_length + 1))


def test_email_accepts_database_length_limit():
    email = f"a@{'b' * 50}.{'c' * 43}.com"

    assert len(email) == 100
    assert TypeAdapter(UserEmail).validate_python(email) == email


def test_email_rejects_value_over_database_limit():
    email = f"a@{'b' * 50}.{'c' * 44}.com"

    assert len(email) == 101
    with pytest.raises(ValidationError):
        TypeAdapter(UserEmail).validate_python(email)
