from django.conf.urls import url

from . import views


app_name = 'tickets'
urlpatterns = [
    url(r'^tickets/(?P<ticket_id>\d+)/$', views.ticket_detail, name='detail'),
    url(r'^$', views.ticket_list, name='list'),
    url(r'^tickets/sell/$', views.ticket_sell, name='sell'),
	url(r'^tickets/(?P<ticket_id>\d+)/manage/$', views.ticket_manage, name='manage'),
]