Learning Django - Week 9 Assignment - Multiple Apps
Create three apps: blogs, surveys and users.
Have the following URL either display a simple HttpResponse or redirect to a different URL for the following apps
    blogs app
        /blogs - display "placeholder to later display all the list of blogs" via HttpResponse. Have this be handled by a method named 'index'.
        /blogs/new - display "placeholder to display a new form to create a new blog" via HttpResponse. Have this be handled by a method named 'new'.
        /blogs/create - Have this be handled by a method named 'create'.  For now, have this url redirect to /blogs.
        /blogs/{{number}} - display 'placeholder to display blog {{number}}.  For example /blogs/15 should display a message 'placeholder to display blog 15'.  Have this be handled by a method named 'show'.
        /blogs/{{number}}/edit - display 'placeholder to edit blog {{number}}.  Have this be handled by a method named 'edit'.
        /blogs/{{number}}/delete - Have this be handled by a method named 'destroy'. For now, have this url redirect to /blogs. 
    surveys app
        /surveys - display "placeholder to display all the surveys created"
        /surveys/new - display "placeholder for users to add a new survey
    users app
        /register - display 'placeholder for users to create a new user record'
        /login - display 'placeholder for users to login' 
        /users/new - have the same method that handles /register also handle the url request of /users/new
        /users - display 'placeholder to later display all the list of users'
        Have the root route (e.g. localhost/) be handled by the index method in the blogs' view file.Have the root route (e.g. localhost/) be handled by the index method in the blogs' view file.

Have the root route (e.g. localhost/) be handled by the index method in the blogs' view file.