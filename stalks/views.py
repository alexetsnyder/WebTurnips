from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views import generic
from .models import StalkWeek
from .forms import AddDayPriceForm, AddStalkWeekForm, AddTurnipStacksForm, SellTurnipStacksForm


class IndexView(generic.ListView):
    template_name = 'stalks/index.html'
    model = StalkWeek


class StalkWeekDetail(generic.DetailView):
    template_name = 'stalks/stalk_week_detail.html'
    model = StalkWeek


def add_stalk_week(request):
    if request.method == 'POST':
        form = AddStalkWeekForm(request.POST)
        if form.is_valid():
            stalk_week = form.save()
            return HttpResponseRedirect(reverse('stalks:stalk_week_detail', args=(stalk_week.id,)))
    else:
        form = AddStalkWeekForm(initial={'current_date': timezone.now()})
    return render(request, 'stalks/stalk_week_form.html', {'form': form})


def add_day_price(request, stalk_week_id):
    if request.method == 'POST':
        form = AddDayPriceForm(request.POST, stalk_week_id=stalk_week_id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('stalks:stalk_week_detail', args=(stalk_week_id,)))
    else:
        form = AddDayPriceForm(initial={'current_date': timezone.now()})
    stalk_week = get_object_or_404(StalkWeek, pk=stalk_week_id)
    return render(request, 'stalks/day_price_form.html', {'stalk_week': stalk_week, 'form': form})


def add_turnip_stacks(request, stalk_week_id):
    if request.method == 'POST':
        form = AddTurnipStacksForm(request.POST, stalk_week_id=stalk_week_id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('stalks:stalk_week_detail', args=(stalk_week_id,)))
    else:
        form = AddTurnipStacksForm(initial={'sell_date': timezone.now()})
    stalk_week = get_object_or_404(StalkWeek, pk=stalk_week_id)
    return render(request, 'stalks/turnip_stacks_form.html', {'stalk_week': stalk_week, 'form': form})


def sell_turnip_stacks(request, stalk_week_id):
    if request.method == 'POST':
        form = SellTurnipStacksForm(request.POST, stalk_week_id=stalk_week_id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('stalks:stalk_week_detail', args=(stalk_week_id,)))
    else:
        form = SellTurnipStacksForm(initial={'sell_date': timezone.now()})
    stalk_week = get_object_or_404(StalkWeek, pk=stalk_week_id)
    return render(request, 'stalks/sell_turnip_stacks_form.html', {'stalk_week': stalk_week, 'form': form})
