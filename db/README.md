
The following command is used to run the mongo DB container, for now. It runs persistently.
`docker run --network=couscous_net --name couscousmongo -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=root mongo`
