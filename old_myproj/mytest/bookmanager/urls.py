from django.urls import path
from . import views

app_name = 'bookmanager'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add/', views.AddView.as_view(), name='book_add'),  # /buukmanager/add
    path('update/<int:pk>/', views.UpdateView.as_view(), name='book_update'),  # buukmanager/update/1
    path('delete/<int:pk>/', views.DeleteView.as_view(),name='book_delete'),  # /buukmanager/delete/1

    path('<int:pk>/impression/', views.ImpressionList.as_view(), name='impression_list'),  # /buukmanager/
    # path('<str:pk>/impression/add/', views.ImpressionAddView.as_view(), name='impression_add'),  # /buukmanager/
    path('<str:pk>/impression/add/', views.impression_edit, name='impression_add'),  # 登録
    ]