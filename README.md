# Grocery-Store

## Overview
Grocery-Store is a full-stack web application that enables users to sign up, log in, and access the website. The project primarily focuses on backend technologies and allows admins to manage the grocery store's inventory through the backend interface. Users can view and manage their shopping carts after making purchases.

## Technologies Used
* HTML
* CSS
* JavaScript
* Flask (Python web framework)
* Jinja2 template engine
* Python
* MongoDB (NoSQL database)
* Swagger for API documentation
* Postman for API testing
* Docker for containerization

## Features
* User signup and login functionality
* JWT authentication for secure access
* CRUD operations (Create, Read, Update, Delete) on the database through the frontend
* Dynamic data rendering using Jinja2 templates
* MongoDB connectivity for efficient data storage
* RESTful APIs with support for GET, PUT, PATCH, DELETE, POST, and OPTIONS
* API documentation with Swagger OpenAPI

## Installation
To set up the project, follow these steps:

1. Install the required libraries from the `requirements.txt` file:
   ```
   pip install -r requirements.txt
   ```
2. Alternatively, use Docker to build an image and run the container locally:
   ```
   docker ps 
   docker build -t <your-tag-for-the-docker-image> .
   docker-compose up
   ```
   The application should be running on the default port of your machine (usually 5000).

## API Documentation
The project provides various APIs for managing grocery store data. You can test them using Postman. To explore the API documentation, run the app and navigate to [Swagger Doc](https://127.0.0.1:5000/swagger).

You can also access the REST API documentation for Github at [Github Docs for REST API](https://docs.github.com/en/rest?apiVersion=2022-11-28).

## Owner
This project is developed by Sumit Bhusan Panda (me).
