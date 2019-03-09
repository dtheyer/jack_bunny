SHELL=/bin/bash

DOCKER_IMAGE_NAME=jack_bunny-evensi

HOST_PORT=7015

build-docker-image:
	docker build -t ${DOCKER_IMAGE_NAME} .

run-docker: build-docker-image
	docker run -d \
		--name ${DOCKER_IMAGE_NAME} \
                -p ${HOST_PORT}:80 \
		--restart always \
		${DOCKER_IMAGE_NAME}

attach-to-docker:
	docker exec -u 0 -it `docker ps | grep ${DOCKER_IMAGE_NAME} | awk '{print $$1;}'` /bin/sh

clear-docker:
	docker stop `docker ps | grep ${DOCKER_IMAGE_NAME} | awk '{print $$1;}'` || true
	docker rm `docker ps -a | grep ${DOCKER_IMAGE_NAME} | awk '{print $$1;}'` || true

read-logs:
	docker exec ${DOCKER_IMAGE_NAME} cat /var/log/nginx/{access,error,jack_bunny}.log

