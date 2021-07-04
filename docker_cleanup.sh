DOCKER_NAME=sse_flask

docker container rm --force ${DOCKER_NAME}
docker image rm --force ${DOCKER_NAME}
