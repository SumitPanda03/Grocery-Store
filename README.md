# Grocery-Store

## OVERVIEW
A project implementing the use of backend and frontend for a Grocery Site.
The admin lets user can singup and then login to the website and access it.
The site is maintained by the backend side and focuses on backend tech stacks.
The admin can then add and update and delete items from the database of the store
The user can also see the cart after buying things

## Technologies used:
* HTML
* CSS
* JS
* FLASK
* JINJA TEMPLATE
* PYTHON
* MONGODB
* SWAGGER
* POSTMAN
* DOCKER

## FEATURES
* SIGNUP
* LOGIN
* JWT AUTHENTICATION
* ADD, CREATE, DELETE, UPDATE IN DATABASE FROM FRONTEND
* JINJA TEMPLATING FOR DYNAMIC DATA ON FRONTEND
* MONGODB CONNECTIVITY
* RESTAPIs: GET, PUT, PATCH, DELETE, POST, OPTIONS
* SWAGGER OPENAPI DOCUMENTATION

## INSTALLATION
There is a **requirements.txt** file that specifices all the libraries to be imported to run this file.
User can run the file using the following command : 
<pre>
'''bash
pip install -r requirements.txt
''' 
</pre>
  
There is also Docker files included which will create an image and a container in your local machine to run the application directly. You must have docker engine installed in your system from the official website - [Docker Download](https://www.docker.com/products/docker-desktop/)
To use this run the following commands in the command line interface(CLI) at the project directory:

'''bash
docker ps 
docker build -t <your tag for the docker image>
docker-compose up
'''

It should be running on the default port of your machine (mostly 5000)


## API Documentation

### APIs used :
* GET
* POST
* PUT
* PATCH
* DELETE
* OPTIONS

You can check the API and test them using POSTMAN service 

To see the Swagger API Documentation, run the app and then navigate to [Swagger Doc](https://127.0.0.1:5000/swagger)

You can access the API Documnetation of Github for RestAPIs from [Github Docs for REST API](https://docs.github.com/en/rest?apiVersion=2022-11-28)


## OWNER
This project is made by Sumit Bhusan Panda(me)
