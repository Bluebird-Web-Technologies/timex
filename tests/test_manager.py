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
    """Test creating a new project"""
    db = manager.db
    db.session().query(models.Project).delete()

    project_name: str = "Test Project"
    manager.new_project(project_name)

    assert db.session().query(exists().where(models.Project.name == project_name))


def test_duplicate_project(manager):
    """Ensure that an exception is raised if two projects have the same name"""
    db = manager.db
    project_name: str = "DUPLICATE_TEST"
    manager.new_project(project_name)

    session = db.session()

    assert get_count(session, project_name) == 1

    # TODO not sure why pytest.raises doesn't work
    correct_exception_raised = False
    try:
        manager.new_project(project_name)
    except Exception as e:  # noqa: BLE001
        correct_exception_raised = type(e).__name__ == "ModelAlreadyExistsException"

    assert correct_exception_raised

    assert get_count(session, project_name) == 1


def test_list_all_projects(manager):
    db = manager.db
    db.session().query(models.Project).delete()

    project_names: tuple = ("first", "second", "third")
    for project in project_names:
        manager.new_project(project)

    projects = manager.all_projects()
    assert len(projects) == len(project_names)


def get_count(session, name) -> int:
    session.query(models.Project).filter_by(name=name).count()
