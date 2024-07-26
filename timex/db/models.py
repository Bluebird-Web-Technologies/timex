from __future__ import annotations

import datetime  # noqa: TCH003

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

    entries: Mapped[list[Entry]] = relationship(back_populates="project")


entry_tag_association_table = Table(
    "entry_tag_association_table",
    Base.metadata,
    Column("timed_entries_id", ForeignKey("timed_entries.id")),
    Column("tags_id", ForeignKey("tags.id")),
)


class Entry(Base):
    __tablename__ = "timed_entries"

    id: Mapped[int] = mapped_column(primary_key=True)

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    project: Mapped[Project] = relationship(back_populates="entries")

    tags: Mapped[list[Tag]] = relationship(
        secondary=entry_tag_association_table,
    )

    starts_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    ends_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
    )

    def __repr__(self) -> str:
        return f"Entries #{self.id}"


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(String(256))
