from __future__ import annotations

import datetime

from db import models
from db.engine import Database


class ProjectManager:
    def __init__(self, db: Database | None = None):
        if db is None:
            self.db = Database()
        else:
            self.db = db

    def new_project(self, project_name: str) -> None:
        """Create a new project."""

        project: models.Project = models.Project(name=project_name)
        self.db.add(project)
        self.db.commit()

    def start_activity(
        self,
        project_name: str,
        description: str | None = None,
        tags: tuple[str] | None = None,
    ) -> None:
        session = self.db.session()

        project = self.find_project(project_name)
        activity = models.Activity(
            project=project,
            starts_at=datetime.datetime.now(tz=datetime.UTC),
            description=description,
        )
        self.db.add(activity)

        if tags:
            tags_to_add = []
            for tag_name in tags:
                tag = session.query(models.Tag).filter_by(name=tag_name).first()

                if not tag:
                    tag = models.Tag(name=tag_name)
                    self.db.add(tag)

                tags_to_add.append(tag)

            activity.tags.extend(tags_to_add)

        self.db.commit()

    def find_project(self, project_name: str) -> models.Project:
        project: models.Project = (
            self.db.session().query(models.Project).filter_by(name=project_name).first()
        )

        # TODO handle no project found
        return project

    def all_projects(self) -> list[str]:
        return self.db.session().query(models.Project.name).all()
