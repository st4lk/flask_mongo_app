from flask_pymongo import PyMongo

mongo = PyMongo()


def create_indexes():
    # Text index for songs search
    mongo.db.songs.create_index([
        ('artist', 'text'),
        ('title', 'text'),
    ])

    # TODO: It may be usefull to create index for song's `level`, but not sure about selectivity
