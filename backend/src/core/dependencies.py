from typing import Annotated

from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db_session
from src.core.schemas import Pagination

DbSession = Annotated[AsyncSession, Depends(get_db_session)]

PaginationDep = Annotated[Pagination, Query()]
