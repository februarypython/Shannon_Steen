from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name="homepage"), #handle the root route
    url(r'^register/$', views.register, name="register"),  #render new.html
    url(r'^login/$', views.login, name="login"), #render login.html
    url(r'^dashboard/$', views.index, name="dashboard"),  #render index.html
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^users/new/$', views.new, name="new_user"), #render new.html
    url(r'^users/create/$', views.create, name="create_user"),
    url(r'^users/edit/$', views.edit, name="edit"), #render edit.html -- this is from user
    url(r'^users/edit/(?P<user_id>\d+)/$', views.edit, name="edit"), #render edit.html -- this is from admin
    url(r'^users/update/(?P<user_id>\d+)/$', views.update, name="update"),
    url(r'^users/show/(?P<user_id>\d+)/$', views.show, name="show"),
    url(r'^users/(?P<user_id>\d+)/destroy/$', views.destroy, name="destroy"),
]