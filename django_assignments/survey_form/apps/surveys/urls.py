from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index), #handle the root route
    url(r'^surveys/$', views.index),
    url(r'^process/$', views.process), #handle form processing
    url(r'^result/$', views.result) #handle form result display
]