The test container currently serves two endpoints, both on localhost<br/>
:500 TLSv1.3<br/>
:600 TLSv1.2<br/>
<br/>
Currently, you can test each endpoint once a container is running with `curl -ssl -v https://localhost:500`, and 600 for TLS1.2
<br/>
To build the container, use the following command:<br/>
`docker build -t couscoustest .`<br/>
In order to run the container, use the following command from this directory. Otherwise, replace `$PWD` with a path to the current directory:<br/>
`docker run -d -p 500:500 -p 600:600 -v $PWD/conf:/etc/nginx/conf.d/ couscoustest`

