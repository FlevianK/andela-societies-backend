#!/bin/bash

COMMIT_HASH=$(git rev-parse --short HEAD)

if [ "$CIRCLE_BRANCH" == 'master' ]; then
    IMAGE_TAG=$COMMIT_HASH
else
    IMAGE_TAG="${CIRCLE_BRANCH}-${COMMIT_HASH}"
fi

echo "====> Store and authenticate with service account"
echo $GCLOUD_SERVICE_KEY | base64 --decode > ${HOME}/gcloud-service-key.json

echo "====> Login to docker registry"

docker login -u _json_key -p "$(cat ${HOME}/gcloud-service-key.json)" https://gcr.io

make release

make tag $IMAGE_TAG

make publish

# TODO: deploy built image to kubernetes cluster