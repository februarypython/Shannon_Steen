from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="course_index"), #handle the root route
    url(r'^new_course$', views.create, name="create_course"), #handle add course post
    url(r'^course/(?P<course_id>\d+)$', views.show, name="show_course"), #handle show course details, comments route
    url(r'^course/(?P<course_id>\d+)/comment$', views.update, name="add_comment"), #handle add comments post
    url(r'^course/(?P<course_id>\d+)/remove$', views.confirm, name="confirm_remove"), #display removal confirmation
    url(r'^course/(?P<course_id>\d+)/destroy$', views.destroy, name="destroy_course"), #delete course
]