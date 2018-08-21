from django.urls import path,include
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

app_name = 'bookmgr'

urlpatterns = [
    # 書籍
    path('booklist/', views.IndexView.as_view(), name='index'),  # 一覧
    path('add/', views.AddView.as_view(), name='book_add'),  # 追加
    path('multiadd/', views.multiAddView.as_view(), name='book_multiadd'),

    path('update/<int:pk>/', views.UpdateView.as_view(), name='book_update'),  # 編集
    path('delete/<int:pk>/', views.DeleteView.as_view(), name='book_delete'),  # 削除
    # ログアウト
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    # IP
    path('ip/',views.ip,name='ip'),

]
