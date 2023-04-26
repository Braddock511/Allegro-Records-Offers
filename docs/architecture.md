The application consists of several components that run in Docker containers. 
The main components are:
1. FastAPI - REST API that provides functionalities for users
2. Vue - a user interface that uses the REST API to fetch and process data
3. PostgreSQL - a database that stores data about users, transactions and other information needed for the application.

The application also uses several external APIs, such as Allegro API, Azure API, ImageKit API and Discogs API.
These components are connected as shown in the architecture diagram:

![alt text](https://ik.imagekit.io/ybcdqxxka/USING/diagram.png?updatedAt=1682529959158)

