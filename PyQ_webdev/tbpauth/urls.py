from django.conf.urls import url

from . import views


app_name = 'tbpauth'
urlpatterns = [
    url(r'^mypage/$', views.mypage, name='mypage'),
    url(r'^mypage/edit/$', views.mypage_edit, name='mypage_edit'),
]
