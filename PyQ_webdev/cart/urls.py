from django.conf.urls import url

from . import views


app_name = 'cart'
urlpatterns = [
    url(r'^tickets/(?P<ticket_id>\d+)/delete', views.cart_delete, name='delete'),
    url(r'^$', views.cart_list, name='list'),
]
