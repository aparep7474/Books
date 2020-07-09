# Project 1

Web Programming with Python and JavaScript

https://www.youtube.com/watch?v=3g0OFEE_Nho

All of the following pages extends the layout.html which contains code for a navbar which changes depending if you have login or not. If you have login you will be presented with a search and log out button on the navbar, but if you haven't login then you will have the sign up and login options. (layout.html)

When you boot up the app you will be presented with a login screen which is the index page, and from there you will be able to go to the sign up page where you can sign up or if you have already been to my app you can login. When you are in the sign up page you will be presented with an error if you enter a username that has already been chosen. If not you will be redirected to the login page where you will be able to enter an existing username and password, and if either is wrong you will be presented with an error page. (log_in.html and sign_up.html)

Once you login you have the opinion to search in the search bar for a book or log out which will clear your session. You can use a post request in the search bar to search up books by isbn, author, or title, and then you will be presented with a results page which displays all books which match that description. If there are no books that match that description you will be taken to a error page (search.html and books.html)

If you click on one of the books then you be taken to the book_isbn.html page. On this page there is the author, isbn, and title of the book, and under those there is the goodreads work ratings count and average score. Below that there is an option to add a review and any other existing reviews that have been added to that book. If you have already added a review and you try to add another you will yet again be taken to an error page. (book_isbn.html)

Finally, if you go to the /api/{isbn} route you will be taken to a page which displays all of the contents of the book page but in json format. If you enter an invalid isbn you will be taken to an error page. (api.html)
