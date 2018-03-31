from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="homepage"), #handle the root route
    url(r'register/$', views.register, name="register"),  #render new.html
    url(r'login/$', views.login, name="login"), #render login.html
    url(r'dashboard/$', views.show, name="dashboard"),  #render index.html
    url(r'logout/$', views.logout, name="logout"),
]