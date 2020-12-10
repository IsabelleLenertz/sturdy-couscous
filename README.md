# sturdy-couscous
An web-security audit agent for local and enterprise networks

# Licence information
The autor of this repository do not allow use, modification, or sharing of this sofwarethe software. Please contact any of us to discuss the addition of an open-source licence or private licence.

# Authors
* Isabelle Delmas, 
* Janani Sridhar, 
* Sohrab (aka Robby) Boparai

# Usage Info
## Requirements
- Python 3.9 - we go not guarantee compatibility eith older or more recent versions of python 
- Python libraries -the python packages required are indicated in the sturdycouscous/requirements.txt file which should run automanicaly when creating the couscouscore docker image. If you chose to run from your own container or machine you can install themn using the pip packat manager
- Docker Engine version 19.03.13 or later - depending on your version, you might need to add the following config to your Docker Engine:
'''  "features": {
    "buildkit": false
  }'''
- An Internet connection **preferably with a VPN**

## Usage
* Frist, from this folder, make sure your system can build and run the containers using the run_db_test.sh
''' chmod +x run_db_test.sh
    ./run_db_test.sh '''
* Next, start a sutrdycouscous core, a sturdycouscous db container - the images and docker network should have been built by run_test_db.sh
'''docker run --network=couscous_net --name couscousmongo -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=root mongo'''
'''docker run -it sturdy-couscous /bin/bash'''
* You should now have a bash session into the sturdycouscous core container from which you can run the application. metods to run the different stages of the appication are in the 'Driver.py file:
```
import sys
sys.path.append("/usr/src/app/sturdy-couscous/sturdycouscous")
import Driver.py
# To run all the stages
Drvier.run_all()
# For the following commands, if no arguments are provided the program will use the sample file provided

# To generate a list of urls to visite from a history file
Driver.get_dataset(filename, generations, is_csv, index, separator)

# To train the classifier
train_classifier(training_set)

# To run the Analysis
run_analysis(filename)

# To print the analysis report
print_report()

# To import the amaylisi data previously exported (default uses the same default location as export_databse)
import_data(filename)
import_classification_data()

# To export the database content to db/domain_info.json and db/categories.json - this will overwrite the samples provided
export_database()

# Configuration for Mongo Client connection, as well as paths for data input and output files, can be configured by adjusting the constants in Utils.py

```
