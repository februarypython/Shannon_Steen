from django.conf.urls import url
from . import views

app_name = "communiques"
urlpatterns = [
    url(r'create/(?P<msg_to_id>\d+)/$', views.create, name="create"),
    url(r'show/(?P<user_id>\d+)/$', views.show, name="show"), #show user archived messages
    url(r'update/(?P<message_id>\d+)/$', views.update, name="update"),  # from user initiated archive message
    url(r'edit/(?P<message_id>\d+)/$', views.edit, name="edit"), # auto-updating read status
]