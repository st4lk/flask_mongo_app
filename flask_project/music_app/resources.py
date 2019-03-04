from datetime import datetime

import pymongo
from flask import request, Blueprint
from flask_restful import Api, Resource, marshal_with

from .db import mongo
from .parsers import level_parser, object_id, page_parser, PAGE_SIZE, rating_parser
from .serializers import song_fields

api_songs_blueprint = Blueprint('api_songs', __name__, url_prefix='/songs')
api_songs = Api(api_songs_blueprint)


class SongsList(Resource):

    @marshal_with(song_fields)
    def get(self):
        args = page_parser.parse_args()
        offset = (args.page - 1) * args.page_size
        cursor = mongo.db.songs.find(
            {}, {'ratings': False},
        ).sort(
            '_id', pymongo.DESCENDING,
        ).skip(offset).limit(args.page_size)
        return list(cursor)


class SongsAvgDifficulty(Resource):

    def get(self):
        args = level_parser.parse_args()
        pipeline = [{'$match': {'level': args.level}}] if args.level is not None else []
        pipeline.append({'$group': {'_id': None, 'avg': {'$avg': '$difficulty'}}})
        result = list(mongo.db.songs.aggregate(pipeline))
        if not result:
            return {'message': 'Songs not found'}, 404
        return {'average_difficulty': result[0]['avg']}


class SongsSearch(Resource):

    @marshal_with(song_fields)
    def get(self):
        message = request.args.get('message') or ''
        cursor = mongo.db.songs.find(
            {'$text': {'$search': message}},
            {'score': {'$meta': 'textScore'}, 'ratings': False},
        ).sort(
            [('score', {'$meta': 'textScore'})],
        ).limit(PAGE_SIZE)
        return list(cursor)


class SongsRating(Resource):

    def post(self):
        args = rating_parser.parse_args()
        # Assuming, that 16Mb per document would be enough to store all ratings per song
        result = mongo.db.songs.update_one(
            {'_id': args.song_id},
            {'$push': {
                'ratings': {
                    'rating': args.rating, 'created_at': datetime.utcnow(),
                },
            }},
        )
        if not result.matched_count:
            return {'message': 'Song not found'}, 404
        return {'result': 'ok'}, 201


class SongsAvgRating(Resource):

    def get(self, song_id):
        try:
            song_id = object_id(song_id)
        except ValueError:
            return {'message': 'Bad request'}, 400
        pipeline = [
            {'$match': {'_id': song_id}},
            {'$project': {'_id': 0, 'ratings.rating': 1}},
            {'$unwind': '$ratings'},
            {'$group': {
                '_id': None,
                'average': {'$avg': '$ratings.rating'},
                'lowest': {'$min': '$ratings.rating'},
                'highest': {'$max': '$ratings.rating'},
            }},
        ]
        result = list(mongo.db.songs.aggregate(pipeline))
        if not result:
            return {'message': 'Ratings not found'}, 404
        avg_rating_data = result[0]
        avg_rating_data.pop('_id')
        return avg_rating_data


api_songs.add_resource(SongsList, '', endpoint='list')
api_songs.add_resource(SongsAvgDifficulty, '/avg/difficulty', endpoint='avg_difficulty')
api_songs.add_resource(SongsSearch, '/search', endpoint='search')
api_songs.add_resource(SongsRating, '/rating', endpoint='add_rating')
api_songs.add_resource(SongsAvgRating, '/avg/rating/<song_id>', endpoint='avg_rating')
