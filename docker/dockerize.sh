#!/bin/sh

DIR="$(dirname "$(readlink -f "$0")")"
VERSION=$(cat ${DIR}/version)
CONTAINER_NAME=${GITHUB_REPOSITORY}-py

build() {
  echo "Start build ${VERSION}"

  docker build \
    -t ${CONTAINER_NAME}:${VERSION} \
    -t ${CONTAINER_NAME}:latest \
    -f ${DIR}/Dockerfile ${DIR}/..
}

push() {
  echo "Pushing ${VERSION}"

  docker push ${CONTAINER_NAME}:${VERSION}
  docker push ${CONTAINER_NAME}:latest
}

clean() {
  echo "Cleaning ${VERSION}"

  docker rmi ${CONTAINER_NAME}:${VERSION}
  docker rmi ${CONTAINER_NAME}:latest
}

$1
