from django.contrib import admin
from .models import StalkWeek, TurnipStacks, DayPrices


class TurnipStackInLine(admin.StackedInline):
    model = TurnipStacks


class DayPricesTabular(admin.TabularInline):
    model = DayPrices


class StalkWeekAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['buy_price']}),
        ('Week Dates', {'fields': ['start_date', 'end_date']}),
    ]
    inlines = [TurnipStackInLine, DayPricesTabular]


admin.site.register(StalkWeek, StalkWeekAdmin)

