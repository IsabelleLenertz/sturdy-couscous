#!/bin/bash
set -ax

# This script runs the composition that connects an instance of the core Garbanzo image to the mongo.db image in the most basic way possible

# Run this from the current directory for ideal results

source couscous.env

function makeNetwork() {

	docker network create $NETWORK_NAME

}

function launchMongo() {

	docker build -t $MONGO_IMAGE_TAG $PWD/db/

	docker run -d --network=$NETWORK_NAME --name $MONGO_CONTAINER_NAME -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=root -h $MONGO_CONTAINER_NAME $MONGO_IMAGE_TAG
}

function launchCore() {

	docker build -t $CORE_IMAGE_TAG $PWD/sturdycouscous/

	docker run -it -v $PWD/:/usr/src/app --network=$NETWORK_NAME --name $CORE_CONTAINER_NAME --link $MONGO_CONTAINER_NAME $CORE_IMAGE_TAG /bin/bash

}

function cleanUp() {

	docker rm -f $CORE_CONTAINER_NAME

	docker rm -f $MONGO_CONTAINER_NAME

	docker volume rm $(docker volume ls -qf dangling=true)

}



makeNetwork

launchMongo

sleep 5

launchCore

cleanUp

