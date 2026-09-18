"""Populate the development database with deterministic synthetic data."""

from datetime import UTC, datetime, timedelta

from sqlalchemy import select

from src.category.model import Category, CategoryTypeEnum
from src.chapter.models import Chapter
from src.core.database import sessionmaker
from src.country.models import Country
from src.language.models import Language
from src.novel.models import Novel, NovelCategories, NovelStatus, NovelType
from src.teams.models import Team, TeamType, TeamUserRole, TeamUsers
from src.users.models import User, UserProfile, UserRoleEnum
from src.users.utils import get_password_hash

USERS = (
    ("seed_admin", "seed_admin@example.com", "Seed Admin", UserRoleEnum.ADMIN),
    ("seed_reader", "seed_reader@example.com", "Seed Reader", UserRoleEnum.COMMON),
    ("seed_author", "seed_author@example.com", "Seed Author", UserRoleEnum.MANAGER),
)
LANGUAGES = ("English", "Russian", "Japanese", "Korean")
COUNTRIES = ("United States", "Russia", "Japan", "South Korea")
CATEGORIES = (
    ("Fantasy", CategoryTypeEnum.GENRE),
    ("Romance", CategoryTypeEnum.GENRE),
    ("Adventure", CategoryTypeEnum.GENRE),
    ("Magic", CategoryTypeEnum.TAG),
    ("Cultivation", CategoryTypeEnum.TAG),
    ("Academy", CategoryTypeEnum.TAG),
)
TEAM_NAMES = (
    ("Aurora Translators", TeamType.TRANSLATORS),
    ("North Star Authors", TeamType.AUTHORS),
    ("Open Quill Publishers", TeamType.PUBLISHERS),
)
BASE_NOVEL_TITLES = (
    "The Clockwork Garden",
    "Letters from the Moon",
    "The Last Ember Academy",
    "A Cartographer of Forgotten Roads",
    "The Alchemist's Quiet Summer",
    "Seven Keys to Winter",
    "The Orchard Beyond the Sea",
    "A Crown Made of Starlight",
    "The Librarian of Hollow City",
    "When Rivers Learn to Fly",
    "The Glasswright's Apprentice",
    "A Small Dragon in the Attic",
)
NOVEL_TITLES = BASE_NOVEL_TITLES + tuple(
    f"Seed Chronicle {index:02d}" for index in range(1, 49)
)
CHAPTERS_PER_NOVEL = 5


async def _get_or_create_reference_data() -> tuple[
    list[User], list[Language], list[Country], list[Category], list[Team]
]:
    async with sessionmaker() as session:
        users: list[User] = []
        for login, email, nickname, role in USERS:
            user = await session.scalar(select(User).where(User.login == login))
            if user is None:
                user = User(
                    login=login,
                    email=email,
                    password_hash=get_password_hash("SeedPassword123!"),
                    role=role,
                )
                session.add(user)
                await session.flush()

            profile = await session.scalar(
                select(UserProfile).where(UserProfile.user_id == user.id)
            )
            if profile is None:
                session.add(UserProfile(user_id=user.id, nickname=nickname))
            users.append(user)

        languages: list[Language] = []
        for name in LANGUAGES:
            language = await session.scalar(
                select(Language).where(Language.name == name)
            )
            if language is None:
                language = Language(name=name)
                session.add(language)
                await session.flush()
            languages.append(language)

        countries: list[Country] = []
        for name in COUNTRIES:
            country = await session.scalar(select(Country).where(Country.name == name))
            if country is None:
                country = Country(name=name)
                session.add(country)
                await session.flush()
            countries.append(country)

        categories: list[Category] = []
        for name, category_type in CATEGORIES:
            category = await session.scalar(
                select(Category).where(Category.name == name)
            )
            if category is None:
                category = Category(name=name, type=category_type)
                session.add(category)
                await session.flush()
            categories.append(category)

        teams: list[Team] = []
        for index, (name, team_type) in enumerate(TEAM_NAMES):
            team = await session.scalar(select(Team).where(Team.name == name))
            if team is None:
                team = Team(
                    name=name,
                    type=team_type,
                    creator_id=users[index % len(users)].id,
                    is_verified=True,
                )
                session.add(team)
                await session.flush()

            membership = await session.scalar(
                select(TeamUsers).where(
                    TeamUsers.team_id == team.id,
                    TeamUsers.user_id == users[index % len(users)].id,
                )
            )
            if membership is None:
                session.add(
                    TeamUsers(
                        team_id=team.id,
                        user_id=users[index % len(users)].id,
                        role=TeamUserRole.CREATOR,
                    )
                )
            teams.append(team)

        await session.commit()
        return users, languages, countries, categories, teams


async def seed() -> None:
    (
        users,
        languages,
        countries,
        categories,
        teams,
    ) = await _get_or_create_reference_data()

    async with sessionmaker() as session:
        for index, title in enumerate(NOVEL_TITLES):
            novel = await session.scalar(select(Novel).where(Novel.title == title))
            team = teams[index % len(teams)]
            language = languages[index % len(languages)]
            country = countries[index % len(countries)]

            if novel is None:
                novel = Novel(
                    title=title,
                    cover_path=f"seed/covers/novel-{index + 1}.jpg",
                    team_id=team.id,
                    language_id=language.id,
                    country_id=country.id,
                    description=(
                        f"A synthetic development novel about {title.lower()}. "
                        "This description exists only for local testing."
                    ),
                    publish_date=datetime.now(UTC) - timedelta(days=index * 14),
                    type=NovelType.ORIGINAL if index % 2 == 0 else NovelType.AUTHORS,
                    status=(
                        NovelStatus.COMPLETED
                        if index % 4 == 0
                        else NovelStatus.CONTINUES
                    ),
                    age_limit=12 if index % 3 else 16,
                    is_approved=index % 5 != 0,
                )
                session.add(novel)
                await session.flush()

            category = categories[index % len(categories)]
            relation = await session.scalar(
                select(NovelCategories).where(
                    NovelCategories.novel_id == novel.id,
                    NovelCategories.category_id == category.id,
                )
            )
            if relation is None:
                session.add(NovelCategories(novel_id=novel.id, category_id=category.id))

            for chapter_number in range(1, CHAPTERS_PER_NOVEL + 1):
                chapter = await session.scalar(
                    select(Chapter).where(
                        Chapter.novel_id == novel.id,
                        Chapter.number == chapter_number,
                    )
                )
                if chapter is None:
                    session.add(
                        Chapter(
                            title=f"Chapter {chapter_number}",
                            number=chapter_number,
                            content=(
                                f"Synthetic chapter {chapter_number} for {title}. "
                                "No external text is used in this fixture."
                            ),
                            is_published=chapter_number < CHAPTERS_PER_NOVEL,
                            novel_id=novel.id,
                            team_id=team.id,
                        )
                    )

        await session.commit()

    print(
        f"Seed complete: {len(USERS)} users, {len(TEAM_NAMES)} teams, "
        f"{len(NOVEL_TITLES)} novels with {CHAPTERS_PER_NOVEL} chapters each."
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(seed())
