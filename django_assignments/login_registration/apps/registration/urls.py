from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="view_index"), #handle the root route
    url(r'^register$', views.create, name="create_user"), #handle the registration route
    url(r'^login$', views.show, name="login_user"), #handle the login route
    url(r'^success$', views.success, name="success"), #handle the successful route
]