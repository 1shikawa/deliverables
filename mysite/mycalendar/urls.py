from django.urls import path
from . import views
from django.contrib.auth import views as auth_views #ログアウトに必要

app_name = 'mycalendar'

urlpatterns = [
    path(
        'month_with_schedule/',
        views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'
    ),
    path(
        'month_with_schedule/<int:year>/<int:month>/',
        views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'
    ),
    path(
        'month_with_schedule/<int:year>/<int:month>/<int:day>',
        views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'
    ),

    # 新規単一登録
    # path(
    #     'month_with_schedule/newadd/<int:year>/<int:month>/<int:day>',
    #     views.NewAdd.as_view(), name='NewAdd'
    # ),
    # 複数登録
    path(
        'month_with_schedule/NewMultiAdd/<int:year>/<int:month>/<int:day>',
        views.NewMultiAdd.as_view(), name='NewMultiAdd'
    ),
    # 編集
    # path(
    #     'month_with_schedule/newedit/<int:pk>',
    #     views.NewEdit.as_view(), name='NewEdit'
    # ),

    # path(
    #     'month_with_schedule/newedit/<int:year>/<int:month>/<int:day>',
    #     views.NewEdit.as_view(), name='NewEdit'
    # ),
    path(
        'month_with_schedule/NewMultiEdit/<int:year>/<int:month>/<int:day>',
        views.NewMultiEdit.as_view(), name = 'NewMultiEdit'
    ),
    # 一覧
    path(
        'inputList/',views.inputList.as_view(), name='inputList'
    ),
    path(
        'MonthlySumList/', views.MonthlySumList.as_view(), name='MonthlySumList'
    ),

    # ログアウト
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),


    path('mycalendar/', views.MyCalendar.as_view(), name='mycalendar'),
    path(
        'mycalendar/<int:year>/<int:month>/<int:day>/', views.MyCalendar.as_view(), name='mycalendar'
    ),
]
