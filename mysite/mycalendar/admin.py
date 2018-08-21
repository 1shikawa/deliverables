from django.contrib import admin
from .models import Schedule,LargeItem,MiddleItem

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('LargeItem', 'summary','kosu','date','totalkosu','register')  # 一覧に出したい項目
    list_display_links = ('LargeItem',)  # 修正リンクでクリックできる項目


admin.site.register(Schedule, ScheduleAdmin)

admin.site.register(LargeItem)
admin.site.register(MiddleItem)
