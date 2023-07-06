# Grocery-Store

A project implementing the use of backend and frontend for a Grocery Site

Tech used:
- HTML
- CSS
- JS
- FLASK
- JINJA TEMPLATE
- PYTHON
- MONGODB
- SWAGGER
- POSTMAN
- DOCKER

It has several operations executed like :
- Signup
- Login
- JWT Authentication
- ADD , CREATE, DELETE, UPDATE IN DATABASE FROM FRONTEND
- JINJA TEMPLATING FOR DYNAMIC DATA ON FRONTEND
- MONGODB CONNECTIVITY
- RESTAPIs : GET, PUT, PATCH, DELETE, POST, OPTIONS
- SWAGGER OPENAPI DOCUMENTATION

There is a requirements.txt file that specifices all the libraries to be imported to run this file.
User can run the file using the following command : 
pip install -r requirements.txt

There is also Docker files included which will create an image and a container in your local machine to run the application directly. You must have docker engine installed in your system from https://www.docker.com/products/docker-desktop/ 
To use this run the following commands in the command line interface(CLI) at the project directory:
docker ps 
docker build -t <your tag for the docker image>
docker-compose up

It should be running on the default port of your machine (mostly 5000)

 running
