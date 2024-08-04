from __future__ import annotations

import datetime

from db import models
from db.engine import Database
from exceptions import ActivityAlreadyActiveError
from exceptions import ModelAlreadyExistsError
from exceptions import ModelNotFoundError


class ProjectManager:
    def __init__(self, db: Database | None = None):
        if db is None:
            self.db = Database()
        else:
            self.db = db

    def new_project(self, project_name: str) -> None:
        """Create a new project."""

        existing_project = (
            self.db.session().query(models.Project).filter_by(name=project_name).first()
        )
        if existing_project:
            raise ModelAlreadyExistsError(project_name)

        project: models.Project = models.Project(name=project_name)
        self.db.add(project)
        self.db.commit()

    def stop_activity(self):
        activity: models.Activity = (
            self.db.session().query(models.Activity).filter_by(is_active=True).first()
        )
        if activity is None:
            raise ModelNotFoundError

        activity.is_active = False
        activity.ends_at = datetime.datetime.now(tz=datetime.timezone.utc)
        self.db.commit()

        return activity.ends_at - activity.starts_at

    def start_activity(
        self,
        project_name: str,
        description: str | None = None,
        tags: tuple[str] | None = None,
    ) -> None:
        session = self.db.session()

        project = self.find_project(project_name)
        active_activities = (
            session.query(models.Activity).filter_by(is_active=True).all()
        )

        # TODO replace all with exists
        if active_activities:
            raise ActivityAlreadyActiveError

        activity = models.Activity(
            project=project,
            starts_at=datetime.datetime.now(tz=datetime.timezone.utc),
            description=description,
            is_active=True,
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

    def current_activity(self):
        """Locate the currently engaged activity"""
        return (
            self.db.session().query(models.Activity).filter_by(is_active=True).first()
        )

    def find_project(self, project_name: str) -> models.Project:
        project: models.Project = (
            self.db.session().query(models.Project).filter_by(name=project_name).first()
        )

        # TODO handle no project found
        return project

    def all_projects(self) -> list[str]:
        return self.db.session().query(models.Project.name).all()
