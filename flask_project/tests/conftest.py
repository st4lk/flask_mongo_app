import os

import pytest

from music_app.app import create_app
from music_app.db import create_indexes, mongo

BASE_DIR = os.path.dirname(__file__)


@pytest.fixture
def app():
    app = create_app(config_name='test')
    return app


@pytest.fixture(scope='function', autouse=True)
def clean_test_db(app):
    # Clean test database before each test.
    mongo.db.client.drop_database(mongo.db.name)
    # Ensure all indexes are created
    create_indexes()
