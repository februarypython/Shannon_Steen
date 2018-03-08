Learning SQL/Flask Connections - Week 8 Assignment
Create a web app that can handle all of the CRUD operations (create, read, update and destroy) for a table.
Have the following 7 routes:
    1. a GET request to /users - calls the index method to display all the users.
    2. GET request to /users/new - calls the new method to display a form allowing users to create a new user. 
    3. GET request /users/<id>/edit - calls the edit method to display a form allowing users to edit an existing user with the given id.
    4. GET /users/<id> - calls the show method to display the info for a particular user with given id.
    5. POST to /users/create - calls the create method to insert a new user record into our database. This POST should be sent from the form on the page /users/new. Redirect to /users/<id> once created.
    6. GET /users/<id>/destroy - calls the destroy method to remove a particular user with the given id. Redirect back to /users once deleted.
    7. POST /users/<id> - calls the update method to process the submitted form sent from /users/<id>/edit. Redirect to /users/<id> once updated.

3.4.18 initial commit
3.7.18 moving files to new directory, updated readme