# Project - SPORTS CATALOG
The project as part of the Udacity Full Stack Nanodegree involves building an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites
Python 3.x is required to execute this program
Download and install vagrant

### Installing
* Download the project zip file locally to your computer and unzip in the directory with vagrant
* CD into the vagrant directory and do "vagrant up" and "vagrant ssh". Then cd /vagrant and cd into the catalog directory
* Execute the below commands to create and populate a sports catalog DB
	* python database_setup.py(creates the DB schema and relationships)
	* python itemscatalogwithusersandtime.py (populates the DB with data)
	* python application.py (executes the application)
* Open the browser with http://localhost:5000/catalog/all - Home Page


### HOW THE SPORTS CATALOG WORKS

* The home page (http://localhost:5000/catalog/all) lists all the sports categories and the latest items added into the categories.
* There is an option to log in. This option is also available on when you go to a page listing all the items in a category or an item description.
* Logging in gives you the ability to create a new item, update an item and delete an item.
* Click on a category to view the items inside the category, choosing an item on this page shows the description.
* JSON Endpoints Examples
	* http://localhost:5000/catalog/all/JSON 
	* http://localhost:5000/catalog/Soccer/items/JSON
(/catalog/<path:category_name>/items/JSON - to view items by category)

### MISCELLANEOUS 
* There is a file called client_secrets.json which stores the key required for Google Authentication and is required for the project.

## Authors
* **Reshma Shanbhag** (https://github.com/reshshanbhag)

## Acknowledgments
* Udacity README course
* Initial Readme template https://gist.github.com/PurpleBooth/109311bb0361f32d87a2
* Restaurant Application from the course 
https://github.com/udacity/Full-Stack-Foundations/tree/master/Lesson-3
