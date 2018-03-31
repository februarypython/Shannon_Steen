from django.conf.urls import url
from . import views

app_name = "communiques"
urlpatterns = [
    url(r'create/(?P<msg_to_id>\d+)/$', views.create, name="create"),
]