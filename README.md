# sturdy-couscous
An web-security audit agent for local and enterprise networks

# Licence information
The autor of this repository do not allow use, modification, or sharing of this sofwarethe software. Please contact any of us to discuss the addition of an open-source licence or private licence.

# Authors
* Isabelle Delmas, 
* Janani Sridhar, 
* Sohrab (aka Robby) Boparai



# To run
Make sure you have docker engine installed and running. Test it with a `docker run hello-world`.<br/>
Once that's verified, navigate to this directory in your terminal, and use the following command to pull the necessary Docker dependencies and build the base image locally.<br/>
`docker build -t sturdy-couscous .`<br/>
After that, use this command to run the container, which will run test_script.py from in the container and output the results to your terminal.<br/>
`docker run -a stdout sturdy-couscous`<br/>
If you'd like to Run the container and have a shell inside of it, use the following command:<br/>
`docker run -it sturdy-couscous /bin/bash`
