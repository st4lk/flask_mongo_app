import json

import click

from .db import mongo


@click.command('load_data')
@click.argument('collection')
@click.argument('file_path')
def load_data(collection: str, file_path: str) -> None:
    with open(file_path) as f:
        initial_data = json.load(f)
    mongo.db[collection].insert_many(initial_data)
