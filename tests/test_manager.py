from pathlib import Path

import pytest
from sqlalchemy import exists

import timex.manager as pm
from timex.db import engine
from timex.db import models


@pytest.fixture(scope="module")
def manager():
    test_db = "test.db"
    # Create an in-memory SQLite database
    db = engine.Database(test_db)
    db.create_schema()
    db.start_engine()

    manager = pm.ProjectManager(db)

    yield manager

    Path(test_db).unlink()


def test_new_project(manager):
    db = manager.db
    db.session().query(models.Project).delete()

    project_name: str = "Test Project"
    manager.new_project(project_name)

    assert db.session().query(exists().where(models.Project.name == project_name))


def test_list_all_projects(manager):
    db = manager.db
    db.session().query(models.Project).delete()

    project_names: tuple = ("first", "second", "third")
    for project in project_names:
        manager.new_project(project)

    projects = manager.all_projects()
    assert len(projects) == len(project_names)
