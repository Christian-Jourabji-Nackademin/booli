# Booli template for Flask (Python) 
Template for flask app used at booli. This code is used to copy into a new project and then used to quickly speed up a new deployment.
In this project we have the following setup

- Local dev in docker
- Logs in json 
- Metrix exposed on /metrics 
- Health exposed on /health
- Deployment with helm to int and prod clusters

## Local devolope
To use the image in local developing do the following

### Install req

```
docker-compose run web pip install 
```


### Run 

```
docker-compose up
```

ore

```
docker-compose run --service-ports web /bin/bash
$python start.py
```



