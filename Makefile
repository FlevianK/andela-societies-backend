PROJECT_NAME := andelasocietiesbackend
REPO_NAME ?= andela-societies-backend

# File names
DOCKER_TEST_COMPOSE_FILE := docker/test/docker-compose.yml

# Docker compose project names
DOCKER_TEST_PROJECT := "$(PROJECT_NAME)test"

## Generate Virtual environment
venv:
	${INFO} "Creating Python Virtual Environment"
	@ python3 -m venv venv
	${SUCCESS} "Virtual Environment has be created successfully, run '. venv/bin/activate' to activate it"
	${INFO} "If you encounter any issues, contact your team lead or add an issue on GitHub"
	@ echo " "

## Generate .env file from the provided sample
env_file:
	@ chmod +x scripts/utils.sh && scripts/utils.sh addEnvFile
	@ echo " "

## Run project test cases
test:env_file
	${INFO} "Creating cache docker volume"
	@ echo " "
	@ docker volume create --name=cache > /dev/null
	${INFO} "Building required docker images for testing"
	@ echo " "
	@ docker-compose -p $(DOCKER_TEST_PROJECT) -f $(DOCKER_TEST_COMPOSE_FILE) build --pull test
	${INFO} "Build Completed successfully"
	@ echo " "
	@ ${INFO} "Running tests in docker container"
	@ yes | docker-compose -p $(DOCKER_TEST_PROJECT) -f $(DOCKER_TEST_COMPOSE_FILE) up test
	${INFO}"Copying test coverage reports"
	@ bash -c 'if [ -d "test-reports" ]; then rm -Rf test-reports; fi'
	@ docker cp $$(docker-compose -p $(DOCKER_TEST_PROJECT) -f $(DOCKER_TEST_COMPOSE_FILE) ps -q test):/application/htmlcov test-reports
	@ ${INFO} "Cleaning workspace after test"
	@ docker-compose -p $(DOCKER_TEST_PROJECT) -f $(DOCKER_TEST_COMPOSE_FILE) down -v

## Destroy test environments
destroy:
	${INFO} "Destroying test environment..."
	@ docker-compose -p $(DOCKER_TEST_PROJECT) -f $(DOCKER_TEST_COMPOSE_FILE) down -v
	${INFO} "Removing dangling images..."
	@ docker images -q -f dangling=true -f label=application=$(PROJECT_NAME) | xargs -I ARGS docker rmi -f ARGS
	${INFO} "Clean complete"

  # COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
NC := "\e[0m"
RESET  := $(shell tput -Txterm sgr0)
# Shell Functions
INFO := @bash -c 'printf $(YELLOW); echo "===> $$1"; printf $(NC)' SOME_VALUE
SUCCESS := @bash -c 'printf $(GREEN); echo "===> $$1"; printf $(NC)' SOME_VALUE
