import datetime
from django.utils.decorators import method_decorator # @method_decoratorに使用
from django.contrib.auth.decorators import login_required # @method_decoratorに使用
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from mycalendar.models import Schedule,LargeItem
from .forms import BS4ScheduleForm, BS4ScheduleNewFormSet, BS4ScheduleEditFormSet
from .basecalendar import (
    MonthCalendarMixin, MonthWithScheduleMixin
)
from django.db.models import Sum
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

# 一括登録
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
        return redirect('mycalendar:month_with_schedule', year=date.year, month=date.month, day=date.day)


# 一括編集
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


@method_decorator(login_required, name='dispatch')
class inputList(generic.TemplateView):
    """入力一覧表示"""
    template_name = 'inputList.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inputList'] = Schedule.objects.all().order_by('date')
        return context


@method_decorator(login_required, name='dispatch')
class sumList(generic.TemplateView):
    """集計一覧表示"""
    template_name = 'sumList.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sumList'] = Schedule.objects.values('date','register').annotate(totalkosu=Sum('kosu')).order_by('date')
        return context