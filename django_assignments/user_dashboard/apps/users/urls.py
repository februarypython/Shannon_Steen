from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="homepage"), #handle the root route
    url(r'^register/$', views.register, name="register"),  #render new.html
    url(r'^login/$', views.login, name="login"), #render login.html
    url(r'^dashboard/new/$', views.new, name="new_user"), #render new.html
    url(r'^dashboard/create/$', views.create, name="create_user"),
    url(r'^dashboard/$', views.show, name="dashboard"),
    # url(r'^dashboard/admin/$', views.show, name="dashboard"),
    url(r'^users/edit/$', views.edit, name="edit"), #render edit.html -- this is from user
    url(r'^users/edit/(?P<user_id>\d+)/$', views.edit, name="edit"), #render edit.html -- this is from admin
    url(r'^users/update/(?P<user_id>\d+)/$', views.update, name="update"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^users/show/(?P<user_id>\d+)', views.show_user, name="show_user"),
    url(r'^dashboard/show/(?P<user_id>\d+)', views.show_user, name="show_user"),
]