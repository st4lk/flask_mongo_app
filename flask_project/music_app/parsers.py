import bson
from flask_restful import inputs, reqparse

PAGE_SIZE = 20


def object_id(value):
    try:
        return bson.ObjectId(value)
    except bson.errors.InvalidId as err:
        raise ValueError(str(err))


page_parser = reqparse.RequestParser()
page_parser.add_argument('page', type=inputs.positive, default=1)
page_parser.add_argument('page_size', type=inputs.positive, default=PAGE_SIZE)


level_parser = reqparse.RequestParser()
level_parser.add_argument('level', type=int)


rating_parser = reqparse.RequestParser()
rating_parser.add_argument('song_id', type=object_id, required=True)
rating_parser.add_argument('rating', type=inputs.int_range(1, 5), required=True)
