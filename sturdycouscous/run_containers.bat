docker network create mynet
powershell docker run -it --name=testc --net=mynet --ip=172.18.0.2 --hostname=core.loc testimage /bin/bash
powershell docker run -it --name=oldtestc --net=mynet --ip=172.18.0.3 --hostname=old.loc oldtest /bin/bash