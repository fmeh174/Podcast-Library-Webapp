import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from podcast.adapters import database_repository, repo_populate
from podcast.adapters.orm import *
from path_utils.utils import get_project_root

# Paths to test data and database URIs
TEST_DATA_PATH = get_project_root() / "tests" / "data"
TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///podcast-test.db'


@pytest.fixture
def database_engine():
    """Set up a file-based SQLite database for testing."""
    clear_mappers()

    # Create an engine for the SQLite file-based database
    engine = create_engine(TEST_DATABASE_URI_FILE)
    mapper_registry.metadata.create_all(engine)  # Conditionally create database tables

    # Clear existing data from all tables before running the tests
    with engine.connect() as connection:
        for table in reversed(mapper_registry.metadata.sorted_tables):
            connection.execute(table.delete())

    # Map the domain model to the database tables
    map_model_to_tables()

    # Create a session factory for managing database connections
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)

    # Create a SQLAlchemy repository to interact with the database
    repo_instance = database_repository.SqlAlchemyRepository(session_factory)
    database_mode = True

    # Populate the database with test data
    repo_populate.populate(TEST_DATA_PATH, repo_instance, database_mode)

    # Yield the engine to be used in tests
    yield engine

    # Drop all tables after the tests finish
    mapper_registry.metadata.drop_all(engine)


@pytest.fixture
def session_factory():
    """Set up an in-memory SQLite database for fast database testing."""
    clear_mappers()

    # Create an in-memory SQLite engine
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    mapper_registry.metadata.create_all(engine)  # Create tables in memory
    map_model_to_tables()

    # Clear any pre-existing data in the tables
    with engine.connect() as connection:
        for table in reversed(mapper_registry.metadata.sorted_tables):
            connection.execute(table.delete())

    # Create and return a session factory
    SessionFactory = sessionmaker(bind=engine)
    return SessionFactory


@pytest.fixture
def empty_session():
    """Set up an empty in-memory SQLite database for testing without any preloaded data."""
    clear_mappers()

    # Create an in-memory SQLite engine
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)

    # Create all tables using mapper_registry's metadata
    mapper_registry.metadata.create_all(engine)  # Create tables in memory

    # Create a session for the in-memory database
    session_factory = sessionmaker(bind=engine)
    session = session_factory()

    # Delete all rows in all tables using ORM methods instead of raw SQL
    for table in reversed(mapper_registry.metadata.sorted_tables):
        session.query(table).delete()

    # Map the models to tables
    map_model_to_tables()

    # Yield the session to be used in tests
    yield session

    # Clean up: drop all tables after the test finishes
    mapper_registry.metadata.drop_all(engine)
