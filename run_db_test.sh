# This script runs the composition that connects an instance of the core Garbanzo image to the mongo.db image in the most basic way possible

# Run this from the current directory for ideal results



NETWORK_NAME=couscous_net

CORE_IMAGE_TAG=couscous_image

MONGO_IMAGE_TAG=couscous_mongo_image

CORE_CONTAINER_NAME=couscouscore

MONGO_CONTAINER_NAME=couscousmongo





function makeNetwork() {

	docker network create $NETWORK_NAME

}

function launchMongo() {

	docker build -t $MONGO_IMAGE_TAG $PWD/db/

	docker run -d --network=$NETWORK_NAME --name $MONGO_CONTAINER_NAME -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=root -h $MONGO_CONTAINER_NAME $MONGO_IMAGE_TAG
}

function launchCore() {

	docker build -t $CORE_IMAGE_TAG $PWD/sturdycouscous/

	docker run -v $PWD/:/usr/src/app --network=$NETWORK_NAME --name $CORE_CONTAINER_NAME --link $MONGO_CONTAINER_NAME $CORE_IMAGE_TAG

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

