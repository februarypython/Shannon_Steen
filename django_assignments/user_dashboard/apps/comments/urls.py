from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^create/(?P<msg_id>\d+)/$', views.create, name="create"),
]