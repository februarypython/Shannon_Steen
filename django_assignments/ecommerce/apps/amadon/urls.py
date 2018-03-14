from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index), #handle the root route
    url(r'amadon/$', views.index),
    url(r'amadon/cart$', views.show_cart),    
    url(r'amadon/add/(?P<item_id>\d+)/$', views.add),
    url(r'amadon/update/(?P<item_id>\d+)/$', views.update),
    url(r'amadon/remove/(?P<item_id>\d+)/$', views.remove),
    url(r'amadon/checkout/', views.checkout),
    url(r'amadon/order_details/(?P<order_id>\d+)/$', views.show_order),
]