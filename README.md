Flask project with mongoDB
==========================

### Requirements

- Docker (tested on Docker Desktop v2.0.0.3, Engine: 18.09.2)
- make (tested on GNU Make 3.81)


### How to run

#### Run mongodb

```bash
make mongo-run
```

#### Populate initial data (in another terminal, need to be done only once)

```bash
COMMAND='load_data songs data/initial_songs.json' make command
```

#### Run api service

```bash
make run
```

#### Run tests

```bash
make test
```

### Check resources

- GET [http://127.0.0.1:5000/songs](http://127.0.0.1:5000/songs)
- GET [http://127.0.0.1:5000/songs/avg/difficulty](http://127.0.0.1:5000/songs/avg/difficulty)
- GET [http://127.0.0.1:5000/songs/search?message=waki](http://127.0.0.1:5000/songs/search?message=waki)
- POST [http://127.0.0.1:5000/songs/rating](http://127.0.0.1:5000/songs/rating) `{"song_id": "<song_id>", "rating": 5}`
- GET [http://127.0.0.1:5000/songs/avg/rating/<song_id>](http://127.0.0.1:5000/songs/avg/rating/<song_id>)

### Other useful commands

- Access database using mongo client

    ```bash
    make mongo-client
    ```

- Custom database port (27050 will be used by default):

    ```bash
    DB_PORT=27090 make mongo-run
    ```

    Note: you have to define the port for other commands as well, for example `DB_PORT=27090 make run`

- Run specific test (check [pytest docs](https://docs.pytest.org/en/latest/usage.html) for details):

    ```bash
    TEST_ARGS='-k test_songs_avg_difficulty' make test
    ```

### TODO

- Define docker compose
- Define CI script to run tests automatically
- Check permissions in mongodb
