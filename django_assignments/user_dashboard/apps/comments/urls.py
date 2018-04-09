from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^create/(?P<msg_id>\d+)/$', views.create, name="create"),
    url(r'^destroy/(?P<cmt_id>\d+)/$', views.destroy, name="destroy"),
]