from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
import datetime
from django.utils import timezone
from django.views import generic
from .models import StalkWeek, DayPrices, TurnipStack


class IndexView(generic.ListView):
    template_name = 'stalks/index.html'
    model = StalkWeek


class StalkWeekDetail(generic.DetailView):
    template_name = 'stalks/stalk_week_detail.html'
    model = StalkWeek


def form_create_stalk_week(response):
    return render(response, 'stalks/create_stalk_week.html', {'now': timezone.now().date().strftime('%Y-%m-%d')})


class WeekDay:
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


SUNDAY_TIMEDELTA = {
    WeekDay.MONDAY: -1,
    WeekDay.TUESDAY: -2,
    WeekDay.WEDNESDAY: -3,
    WeekDay.THURSDAY: -4,
    WeekDay.FRIDAY: -5,
    WeekDay.SATURDAY: -6,
    WeekDay.SUNDAY: 0,
}


def get_sunday(now):
    return now + datetime.timedelta(SUNDAY_TIMEDELTA[datetime.date.weekday(now)])


def get_saturday(now):
    return now + datetime.timedelta(SUNDAY_TIMEDELTA[datetime.date.weekday(now)] + 6)


def create_stalk_week(start_date, end_date, buy_price):
    return StalkWeek(start_date=start_date, end_date=end_date, buy_price=buy_price)


def create_day_price(stalk_week_id, date, price_before_noon, price_after_noon):
    return DayPrices(
        stalk_week_id=stalk_week_id,
        price_date=date,
        sell_price_before_noon=price_before_noon,
        sell_price_after_noon=price_after_noon)


def create_turnip_stacks(stalk_week_id, sell_price, turnip_stacks):
    turnips = []
    for i in range(turnip_stacks):
        turnips.append(TurnipStack(stalk_week_id=stalk_week_id, sell_price=sell_price))
    return turnips


def new_stalk_week(request):
    turnip_price = int(request.POST['TurnipPrice'])
    turnip_count = int(request.POST['TurnipCount'])
    week_date = datetime.datetime.strptime(request.POST['WeekDate'], '%Y-%m-%d')
    stalk_week = create_stalk_week(get_sunday(week_date), get_saturday(week_date), turnip_price)
    stalk_week.save()
    turnip_stacks = create_turnip_stacks(stalk_week.id, 0, turnip_count)
    for turnip_stack in turnip_stacks:
        turnip_stack.save()
    return HttpResponseRedirect(reverse('stalks:stalk_week_detail', args=(stalk_week.id,)))
