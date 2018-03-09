from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),  #handle the root route
    url(r'^random_word/$', views.index),  #handle random_word route
    url(r'^random_word/reset$', views.reset),  #handle reset route
]