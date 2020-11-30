# This script runs the composition that connects an instance of the core Garbanzo image to the mongo.db image in the most basic way possible
# Run this from the current directory for ideal results

NETWORK_NAME=db_default
CORE_CONTAINER_NAME=garbanzocore
MONGO_CONTAINER_NAME=garbanzomongo

function makeNetwork() {
	docker network create $NETWORK_NAME 
}

function launchMongo() {
	docker build -t dbtestimage $PWD/db/.
	docker run --network=$NETWORK_NAME --name $MONGO_CONTAINER_NAME -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=root -h py-mongo dbtestimage &
}

function launchCore() {
	docker build -t sturdy-couscous $PWD/Garbanzo/.
	docker run --network=$NETWORK_NAME --name $CORE_CONTAINER_NAME --link $MONGO_CONTAINER_NAME sturdy-couscous
}

function cleanUp() {
	docker rm -f $CORE_CONTAINER_NAME
	docker rm -f $MONGO_CONTAINER_NAME
	docker volume rm $(docker volume ls -qf dangling=true)
}

makeNetwork
launchMongo
launchCore
cleanUp
