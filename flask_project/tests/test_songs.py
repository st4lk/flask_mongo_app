from flask_restful import url_for

from music_app.db import mongo


def test_songs_list(client):
    mongo.db.songs.insert_many([{'artist': f'Lenon #{i}'} for i in range(10)])
    res = client.get(url_for('api_songs.list'))
    assert res.status_code == 200
    assert len(res.json) == 10


def test_songs_list_pagination(client):
    mongo.db.songs.insert_many([{'artist': f'Lenon #{i}'} for i in range(25)])
    res = client.get(url_for('api_songs.list', page=2))
    assert res.status_code == 200
    expected_artists = [{'artist': f'Lenon #{i}'} for i in reversed(range(0, 5))]  # descending
    received_artists = [{'artist': doc['artist']} for doc in res.json]
    assert received_artists == expected_artists


def test_songs_avg_difficulty(client):
    mongo.db.songs.insert_many([
        {'difficulty': 1.0},
        {'difficulty': 2.0},
        {'difficulty': 3.0},
    ])
    res = client.get(url_for('api_songs.avg_difficulty'))
    assert res.status_code == 200
    assert res.json['average_difficulty'] == 2.0


def test_songs_avg_difficulty_with_level(client):
    mongo.db.songs.insert_many([
        {'difficulty': 1.0, 'level': 1},
        {'difficulty': 2.0, 'level': 2},
        {'difficulty': 3.0, 'level': 2},
    ])
    res = client.get(url_for('api_songs.avg_difficulty') + '?level=2')
    assert res.status_code == 200
    assert res.json['average_difficulty'] == 2.5


def test_songs_search(client):
    mongo.db.songs.insert_many([
        {'artist': 'The Yousicians', 'title': 'Lycanthropic Metamorphosis'},
        {'artist': 'Mr Fastfinger', 'title': 'Awaki-Waki'},
    ])
    res = client.get(url_for('api_songs.search') + '?message=fastfinger waki')
    assert res.status_code == 200
    assert len(res.json) == 1
    assert res.json[0]['artist'] == 'Mr Fastfinger'


def test_songs_add_rating(client):
    result = mongo.db.songs.insert_one({'artist': 'Mr Fastfinger', 'title': 'Awaki-Waki'})
    song_id = result.inserted_id
    payload = {'song_id': str(song_id), 'rating': 5}
    res = client.post(url_for('api_songs.add_rating'), json=payload)
    assert res.status_code == 201
    song = mongo.db.songs.find_one({'_id': song_id})
    assert len(song['ratings']) == 1
    assert song['ratings'][0]['rating'] == 5


def test_songs_average_rating(client):
    result_1 = mongo.db.songs.insert_one({
        'title': 'Awaki-Waki', 'ratings': [
            {'rating': 1, 'aa': 'bb'},
            {'rating': 3},
            {'rating': 5},
        ]
    })
    result_2 = mongo.db.songs.insert_one({
        'title': 'Yaki-yaki', 'ratings': [
            {'rating': 2},
            {'rating': 3},
        ]
    })
    song_1_id = result_1.inserted_id
    song_2_id = result_2.inserted_id
    res = client.get(url_for('api_songs.avg_rating', song_id=str(song_1_id)))
    assert res.status_code == 200
    assert res.json == {'average': 3.0, 'lowest': 1, 'highest': 5}

    res = client.get(url_for('api_songs.avg_rating', song_id=str(song_2_id)))
    assert res.status_code == 200
    assert res.json == {'average': 2.5, 'lowest': 2, 'highest': 3}
