from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase): ...


class DB:
    def __init__(self, url: str, echo: bool = False) -> None:
        self.engine = create_engine(url, echo=echo)

    def init(self):
        self.create_tables()

    def create_tables(self) -> None:
        Base.metadata.create_all(self.engine)

    def get_session(self):
        with Session(self.engine) as session:
            yield session


db = DB("sqlite:///db.sqlite")


DbSession = Annotated[Session, Depends(db.get_session)]
