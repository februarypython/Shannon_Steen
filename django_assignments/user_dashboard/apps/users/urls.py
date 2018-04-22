from django.conf.urls import url
from . import views

app_name = "users"
urlpatterns = [
    url(r'new/$', views.new, name="new"), #render new.html
    url(r'create/$', views.create, name="create"),
    url(r'show/(?P<user_id>\d+)/$', views.show, name="show"),
    url(r'edit/(?P<user_id>\d+)/$', views.edit, name="edit"), #render edit.html
    url(r'update/(?P<user_id>\d+)/$', views.update, name="update"),
    url(r'(?P<user_id>\d+)/destroy/$', views.destroy, name="destroy"),
]