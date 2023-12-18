VERSION  := v1.0.0
GIT_HASH := $(shell git rev-parse --short HEAD)
SERVICE  := ping-pong-service
SRC      := $(shell find . -type f -name '*.py' -not -path "./venv/*" -not -path "./internal/proto_gens/*")

.PHONY: help
help: ### Display this help screen.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: init
init: ### Init the runtime requirements.
	@pip install -r requirements.txt

.PHONY: deps
deps: ### Package the runtime requirements.
	@pip freeze > requirements.txt

.PHONY: pb-fmt
pb-fmt: ### Format the proto files using clang-format.
	@clang-format -i ./protos/*.proto

.PHONY: lint
lint: ### Improve your code style. (pyflakes, pycodestyle, isort)
	@echo "Running import sort..."
	@isort --atomic --multi-line=VERTICAL_HANGING_INDENT ${SRC}
	@echo "Running static code analysis..."
	@pyflakes ${SRC}
	@echo "Running code style check..."
	@pycodestyle ${SRC} --ignore=E131,E402,E501

.PHONY: image
image: ### Compile the runtime docker image.
	@docker build -f ./devops/docker/Dockerfile -t infra-${SERVICE}:${VERSION}-${GIT_HASH} .

.PHONY: local_run
local_run: ### Locally run your service.
	@python server.py --conf=./etc/${SERVICE}-dev.json 2>&1 | tee dev.log

.PHONY: run
run: ### Run your service inside container.
	@cp -f ./etc/${SERVICE}-prod.json ~/.infra-config/${SERVICE}.json
	@(docker run --rm -d --network host --name infra-${SERVICE} \
		-e TZ=Asia/Shanghai \
		-v ~/.infra-config:/config \
		infra-${SERVICE}:${VERSION}-${GIT_HASH} \
		/bin/bash -c "python /app/server.py --conf=/config/${SERVICE}.json")

.PHONY: stop
stop: ### Stop your service inside container.
	@docker rm -f infra-${SERVICE} | true

now=$(shell date "+%Y%m%d%H%M%S")
.PHONY: logs
logs: ### Print logs from you service container.
	@docker logs -f infra-${SERVICE} 2>&1 | tee prod_${now}.log
