from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', views.index),
    url(r'^users/new$', views.new),
    url(r'^register/$', views.new),
    url(r'^users/$', views.show),
]