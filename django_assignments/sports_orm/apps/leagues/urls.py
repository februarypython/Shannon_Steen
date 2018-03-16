from django.conf.urls import url
from . import views

urlpatterns = [
	url(r"^$", views.index, name="index"),
	url(r"^more/", views.get_more, name="get_more"),
	url(r"^make_data/", views.make_data, name="make_data"),
]