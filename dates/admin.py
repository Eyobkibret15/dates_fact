from django.contrib import admin

from dates.models import DateFact


@admin.register(DateFact)
class DateFactAdmin(admin.ModelAdmin):
    ordering = ('-days_checked','month_number', 'day')
