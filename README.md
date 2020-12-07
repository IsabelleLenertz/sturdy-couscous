# sturdy-couscous
An web-security audit agent for local and enterprise networks

# Licence information
The autor of this repository do not allow use, modification, or sharing of this sofwarethe software. Please contact any of us to discuss the addition of an open-source licence or private licence.

# Authors
* Isabelle Delmas, 
* Janani Sridhar, 
* Sohrab (aka Robby) Boparai

# Usage Info
* to run unit tests: $ python -B -m unittest sturdycouscous/unit_tests/src/*
* to run checker unit tests: from the sturdycouscous directory: $ python -m unittest unit_tests/src/CheckTester.py
* to start a container with bash session runnnig: $ docker container run -itd idelmas/sturdy-couscous:latest bash &
* to create and run a container with a mounted volume (ie, uses a folder of the host system): $ docker run -it --rm -v <path to folder> s:\ sturdy-couscous:latest bash
