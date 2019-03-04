from flask_restful import fields

song_fields = {
    'id': fields.String(attribute='_id'),
    'artist': fields.String,
    'title': fields.String,
    'difficulty': fields.Float,
    'level': fields.Integer,
    'released': fields.String,
}
