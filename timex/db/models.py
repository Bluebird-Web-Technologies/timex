from __future__ import annotations

import datetime

from sqlalchemy import Boolean
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

    activities: Mapped[list[Activity]] = relationship(back_populates="project")

    def total_time(self):
        return sum(
            [a.duration() for a in self.activities if a.ends_at],
            datetime.timedelta(),
        )

    def __repr__(self) -> str:
        return self.name


activity_tag_association_table = Table(
    "activity_tag_association_table",
    Base.metadata,
    Column("activities_id", ForeignKey("activities.id")),
    Column("tags_id", ForeignKey("tags.id")),
)


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    project: Mapped[Project] = relationship(back_populates="activities")

    description: Mapped[str] = mapped_column(String(256), nullable=True)

    tags: Mapped[list[Tag]] = relationship(
        secondary=activity_tag_association_table,
    )

    starts_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    ends_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    def duration(self):
        if not self.ends_at:
            return None

        return self.ends_at - self.starts_at

    def __repr__(self) -> str:
        return f"Activity #{self.id}"


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(String(256), nullable=True)
