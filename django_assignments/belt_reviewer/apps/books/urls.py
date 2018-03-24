from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="homepage"), #show homepage
    url(r'^register$', views.register, name="create_user"), #register new user
    url(r'^login$', views.login, name="login_user"), #login existing user
    url(r'^books$', views.show_books, name="book_index"), #show all books (template)
    url(r'^books/add$', views.new, name="new_book"), #show new_book form (template)
    url(r'^books/new$', views.create_book, name="add_book"), #create new book
    url(r'^books/(?P<book_id>\d+)$', views.show_book, name="book_details"), #show single book (template)
    url(r'^books/(?P<book_id>\d+)/review$', views.update, name="add_review"), #add new review
    url(r'^users/(?P<user_id>\d+)$', views.show_user, name="user_details"), #show user (template)
    url(r'^books/(?P<book_id>\d+)/review/(?P<review_id>\d+)$', views.destroy, name="destroy_review"), #delete review
    url(r'^logout$', views.logout, name="logout"), #log user out
]