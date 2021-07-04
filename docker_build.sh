#
DOCKER_NAME=sse_flask

docker build -t ${DOCKER_NAME} . --network host
