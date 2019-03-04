MONGO_DOCKER_IMAGE = 'mongo:4.0.6'
MONGO_DOCKER_NAME = 'mongodb_flask_example'
API_DOCKER_NAME = 'api_flask_example'

MONGO_DB_HOST_PATH = $(PWD)/mongodb_data
API_HOST_PATH = $(PWD)/flask_project

DB_HOST ?= `docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(MONGO_DOCKER_NAME)`
DB_PORT ?= 27050
API_PORT ?= 5000


run-mongo:
	@docker stop $(MONGO_DOCKER_NAME) || true && docker rm -v $(MONGO_DOCKER_NAME) || true
	@docker run -it -p $(DB_PORT):$(DB_PORT) -v $(MONGO_DB_HOST_PATH):/data/db --name $(MONGO_DOCKER_NAME) $(MONGO_DOCKER_IMAGE) --port $(DB_PORT)

mongo-client:
	docker exec -it $(MONGO_DOCKER_NAME) mongo --port $(DB_PORT)

api-docker-run:
	@docker build -t $(API_DOCKER_NAME) ./
	@docker stop $(API_DOCKER_NAME) || true && docker rm -v $(API_DOCKER_NAME) || true
	@docker run -it -p $(API_PORT):$(API_PORT) -e DB_HOST=$(DB_HOST) -e DB_PORT=$(DB_PORT) $(PARAMS) \
			-v $(API_HOST_PATH):/flask_project --name $(API_DOCKER_NAME) $(API_DOCKER_NAME) "$(COMMAND)"

shell:
	$(MAKE) api-docker-run COMMAND="make shell"

devserver:
	$(MAKE) api-docker-run COMMAND="make devserver"

command:
	$(MAKE) api-docker-run COMMAND="make command" PARAMS='-e COMMAND="$(COMMAND)"'

test:
	$(MAKE) api-docker-run COMMAND="make test" PARAMS='-e TEST_ARGS="$(TEST_ARGS)"'

run: devserver
