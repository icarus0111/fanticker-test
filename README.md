## Fanticker Test Project

### Requirements
+ write a backend API that increments a counter
+ the API should be reverse-proxied behind Traefik
+ the API has an endpoint "api/counter"
+ the API increments the counter by 1 when a PUT request arrives at the endpoint
+ the API returns the current value of the counter when a GET request arrives
+ the API persists the counter value in a SQL database
+ GET requests query the database for the value
+ the API must authenticate the user and authorize them for two roles
+ the roles are counter-reader & counter-incrementer.
+ counter-reader can only GET the endpoint
+ counter-incrementer should be able to GET & PUT
+ the API must not have any race condition


### How to start project

+ `docker compose build`
+ `docker compose up`

### Swagger docs

+ `http://0.0.0.0:8000/docs#/`




