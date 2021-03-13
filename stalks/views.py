from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views import generic
from .models import StalkWeek
from .date_helper import DateHelper
from .factory import create_turnip_stacks, create_stalk_week


class IndexView(generic.ListView):
    template_name = 'stalks/index.html'
    model = StalkWeek


class StalkWeekDetail(generic.DetailView):
    template_name = 'stalks/stalk_week_detail.html'
    model = StalkWeek


def form_create_stalk_week(response):
    return render(response, 'stalks/create_stalk_week.html', {'now': timezone.now().date().strftime('%Y-%m-%d')})


def new_stalk_week(request):
    turnip_price = int(request.POST['TurnipPrice'])
    turnip_count = int(request.POST['TurnipCount'])
    week_date = DateHelper(request.POST['WeekDate'], '%Y-%m-%d')
    stalk_week = create_stalk_week(week_date.date, turnip_price)
    create_turnip_stacks(stalk_week.id, 0, turnip_count)
    return HttpResponseRedirect(reverse('stalks:stalk_week_detail', args=(stalk_week.id,)))
