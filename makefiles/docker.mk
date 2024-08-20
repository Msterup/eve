# Docker image name
IMAGE_NAME = warzone_tools
IMAGE_TAG = latest
IMAGE_PATH = .
WORKDIR := warzone_tools
GIT_ROOT := $(shell git rev-parse --show-toplevel)
K8S_MANIFESTS := k8s/

LOCAL_REGISTRY = localhost:5000
REGISTRY_IMAGE_NAME = $(LOCAL_REGISTRY)/$(IMAGE_NAME)

DOCKER_ARGS :=
DOCKER_ARGS += -v $(GIT_ROOT)/$(WORKDIR):/$(WORKDIR)

COMPOSE_PROJECT_NAME = warzone_tools
DJANGO_SERVICE=django
	
# Build the Docker image
build:
	docker-compose build

# Start the Docker Compose services
up: build
	docker-compose -p $(COMPOSE_PROJECT_NAME) up -d

# Stop the Docker Compose services
down:
	docker-compose -p $(COMPOSE_PROJECT_NAME) down

django-it:
	docker run -it --rm $(DOCKER_ARGS) $(IMAGE_NAME) /bin/bash

shell:
	@docker-compose -p $(COMPOSE_PROJECT_NAME) exec $(DJANGO_SERVICE) /bin/bash

.PHONY: all build run stop clean
