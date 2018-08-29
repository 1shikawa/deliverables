import datetime
from django.utils.decorators import method_decorator # @method_decoratorに使用
from django.contrib.auth.decorators import login_required # @method_decoratorに使用
from django.contrib import messages  # メッセージフレームワーク
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from mycalendar.models import Schedule,LargeItem
from .forms import BS4ScheduleForm, BS4ScheduleNewFormSet, BS4ScheduleEditFormSet
from .basecalendar import (
    MonthCalendarMixin, MonthWithScheduleMixin
)
from django.db.models import Sum
from dateutil.relativedelta import relativedelta
import pandas as pd

@method_decorator(login_required, name='dispatch')
class MonthWithScheduleCalendar(MonthWithScheduleMixin, generic.TemplateView):
    """スケジュール付きの月間カレンダーを表示するビュー"""
    template_name = 'month_with_schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """月間カレンダー情報の入った辞書を返す"""
        context['month'] = self.get_month_calendar()
        return context


# 単一登録
# class NewAdd(MonthCalendarMixin,generic.CreateView):
#     template_name = 'newadd.html'
#     form_class = BS4ScheduleForm
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['week'] = self.get_week_calendar()
#         context['month'] = self.get_month_calendar()
#         return context
#
#     def form_valid(self, form):
#         month = self.kwargs.get('month')
#         year = self.kwargs.get('year')
#         day = self.kwargs.get('day')
#         if month and year and day:
#             date = datetime.date(year=int(year), month=int(month), day=int(day))
#         else:
#             date = datetime.date.today()
#         schedule = form.save(commit=False)
#         schedule.register = self.request.user
#         schedule.date = date
#         schedule.save()
#         return redirect('mycalendar:month_with_schedule', year=date.year, month=date.month, day=date.day)

"""一括登録・登録後表示機能"""
@method_decorator(login_required, name='dispatch')
class NewMultiAdd(MonthCalendarMixin, generic.FormView):
    template_name = 'multiAdd.html'
    # form_class = BS4ScheduleFormSet
    success_url = reverse_lazy('mycalendar:month_with_schedule')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['week'] = self.get_week_calendar()
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        indate = str(year) + '年' + str(month) + '月' + str(day) + '日'
        date = datetime.date(year=int(year), month=int(month), day=int(day))
        context['indate'] = indate
        context['month'] = self.get_month_calendar()
        context['LargeItem'] = LargeItem.objects.all()
        context['registered'] = Schedule.objects.filter(date=date).filter(register=str(self.request.user))
        try:
            totalkosu = Schedule.objects.filter(date=date).filter(register=str(self.request.user)).first()
            context['totalkosu'] = totalkosu
        except:
            context['totalkosu'] = 0
        return context

    def get_form(self, form_class=None):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = str(year) + '-' + str(month) + '-' + str(day)
        return BS4ScheduleNewFormSet(self.request.POST or None,
                                     queryset=Schedule.objects.none())

    def form_valid(self, form):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        # for fm in form:
        #     schedule = fm.save(commit=False)
        #     # schedule.register = self.request.user
        #     schedule.date = date
        #     schedule.save()
        # return redirect('mycalendar:month_with_schedule', year=date.year, month=date.month, day=date.day)
        # return super().form_valid(form)

        instances = form.save(commit=False)
        # 新たに作成されたscheduleと更新されたscheduleを取り出して、新規作成or更新処理
        for schedule in instances:
            schedule.register = str(self.request.user)
            schedule.date = date
            schedule.save()
        # 総時間をkosuを合計してカラムに登録
        kosuBydate = Schedule.objects.filter(date=date).values('date', 'register').annotate(totalkosu=Sum('kosu'))
        for i in kosuBydate:
            if i['register'] == str(self.request.user):
                total = i['totalkosu']

        for row in Schedule.objects.filter(date=date).filter(register=str(self.request.user)):
            row.totalkosu = int(total)
            row.save()
        messages.success(self.request, date.strftime('%Y年%m月%d日')+"に新規登録しました。")
        # return redirect('mycalendar:month_with_schedule', year=date.year, month=date.month, day=date.day)
        return redirect('mycalendar:NewMultiAdd',year=date.year,month=date.month,day=date.day)


"""一括編集機能"""
@method_decorator(login_required, name='dispatch')
class NewMultiEdit(MonthCalendarMixin, generic.FormView):
    template_name = 'multiEdit.html'
    # form_class = BS4ScheduleFormSet
    success_url = reverse_lazy('mycalendar:month_with_schedule')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['week'] = self.get_week_calendar()
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        indate = str(year) + '年' + str(month) + '月' + str(day) + '日'
        context['month'] = self.get_month_calendar()
        context['indate'] = indate
        context['LargeItem'] = LargeItem.objects.all()
        return context

    def get_form(self, form_class=None):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = str(year) + '-' + str(month) + '-' + str(day)
        return BS4ScheduleEditFormSet(self.request.POST or None,
                                      queryset=Schedule.objects.filter(date=date,register=self.request.user))
        # ,register=self.request.user))

    # def form_valid(self, form):
    #     month = self.kwargs.get('month')
    #     year = self.kwargs.get('year')
    #     day = self.kwargs.get('day')
    #     if month and year and day:
    #         date = datetime.date(year=int(year), month=int(month), day=int(day))
    #     else:
    #         date = datetime.date.today()
    #     for fm in form:
    #         schedule = fm.save(commit=False)
    #         # schedule.register = self.request.user
    #         schedule.date = date
    #         schedule.save()
    #     return redirect('mycalendar:month_with_schedule', year=date.year, month=date.month, day=date.day)
    # return super().form_valid(form)

    def form_valid(self, form):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        # instancesは、新たに作成されたscheduleと更新されたscheduleが入ったリスト
        instances = form.save(commit=False)

        # まず、削除チェックがついたscheduleを取り出して削除
        for schedule in form.deleted_objects:
            schedule.delete()

        total = 0
        # 新たに作成されたscheduleと更新されたscheduleを取り出して、新規作成or更新処理
        for schedule in instances:
            schedule.register = str(self.request.user)
            schedule.date = date
            schedule.save()

        kosuBydate = Schedule.objects.filter(date=date).values('date','register').annotate(totalkosu=Sum('kosu'))
        for i in kosuBydate:
            if i['register'] == str(self.request.user):
                total = i['totalkosu']

        for row in Schedule.objects.filter(date=date).filter(register=str(self.request.user)):
            row.totalkosu = int(total)
            row.save()
        messages.success(self.request, date.strftime('%Y年%m月%d日') + "を更新しました。")
        return redirect('mycalendar:month_with_schedule', year=date.year, month=date.month, day=date.day)
        # return super().form_valid(form)


# class NewEdit(MonthCalendarMixin,generic.UpdateView):
#     model = Schedule
#     template_name = 'newedit.html'
#     form_class = BS4ScheduleForm
#     # success_url = reverse_lazy('mycalendar:month_with_schedule')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['week'] = self.get_week_calendar()
#         context['month'] = self.get_month_calendar()
#         return context
#
#     def form_valid(self, form):
#         month = self.kwargs.get('month')
#         year = self.kwargs.get('year')
#         day = self.kwargs.get('day')
#         if month and year and day:
#             date = datetime.date(year=int(year), month=int(month), day=int(day))
#         else:
#             date = datetime.date.today()
#         schedule = form.save(commit=False)
#         schedule.date = date
#         schedule.save()
#         return redirect('mycalendar:month_with_schedule', year=date.year, month=date.month, day=date.day)

@method_decorator(login_required, name='dispatch')
class MyCalendar(MonthCalendarMixin, generic.CreateView):
    """月間カレンダー、週間カレンダー、スケジュール登録画面のある欲張りビュー"""
    template_name = 'mycalendar.html'
    form_class = BS4ScheduleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['week'] = self.get_week_calendar()
        """月間カレンダー情報の入った辞書を返す"""
        context['month'] = self.get_month_calendar()
        return context

    def form_valid(self, form):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        schedule = form.save(commit=False)
        schedule.date = date
        schedule.save()
        return redirect('mycalendar', year=date.year, month=date.month, day=date.day)


# @method_decorator(login_required, name='dispatch')
# class inputList(generic.TemplateView):
#     """入力一覧表示"""
#     template_name = 'inputList.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['inputList'] = Schedule.objects.all().order_by('date')
#         return context

@method_decorator(login_required, name='dispatch')
class inputList(generic.ListView):
    model = Schedule
    context_object_name = 'inputList'
    template_name = 'inputList.html'

    def get_queryset(self):
        queryset = Schedule.objects.all().order_by('date')
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(date__month=keyword)
        return queryset


@method_decorator(login_required, name='dispatch')
class MonthlySumList(generic.ListView):
    """月次集計一覧表示"""
    # model = Schedule
    # context_object_name = 'MonthlySumList'
    template_name = 'MonthlySumList.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """外部キーの表示名をidではなく、名前にする→__name"""
        today = datetime.date.today()
        first_of_thismonth = today + relativedelta(day=1)
        # context['MonthlySumList'] = Schedule.objects.select_related().values('date','LargeItem__name','register').annotate(MonthlySum=Sum('kosu')).order_by('register','LargeItem')
        # context['MonthlySumList'] = Schedule.objects.select_related().filter(date__range=(first_of_thismonth,today)).values('date', 'LargeItem__name','register').annotate(MonthlySum=Sum('kosu')).order_by('register', 'LargeItem')
        sum_of_thismonth = Schedule.objects.select_related().filter(date__range=(first_of_thismonth, today))
        s = sum_of_thismonth.values('LargeItem__name','register').annotate(MonthlySum=Sum('kosu')).order_by('register', 'LargeItem')
        for i in s:
            context['MonthlySumList'] = i['MonthlySum']



        # keyword = self.request.GET.get('keyword')
        # if keyword:
            # year,month = keyword.split('-')
            # context['MonthlySumList'] = Schedule.objects.filter(date__year=year).filter(date__month=month).values('date','LargeItem__name', 'register').annotate(MonthlySum=Sum('kosu'))
        return context