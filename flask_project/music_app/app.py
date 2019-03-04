import os
from typing import Optional

from flask import Flask

from .commands import load_data
from .config import config_map
from .db import mongo, create_indexes
from .resources import api_songs_blueprint


__all__ = ('create_app', )


def create_app(config_name: Optional[str] = None) -> Flask:
    app = Flask(__name__)
    config_name = config_name or os.environ.get('FLASK_ENV')
    app.config.from_object(config_map[config_name])

    mongo.init_app(app)
    app.register_blueprint(api_songs_blueprint)
    app.cli.add_command(load_data)

    # Ensure all indexes are created
    create_indexes()

    return app
