from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.views import generic
from .models import StalkWeek
from .forms import AddDayPriceForm, AddStalkWeekForm, AddTurnipStacksForm
from .date_helper import DateHelper


class IndexView(generic.ListView):
    template_name = 'stalks/stalk_week_list.html'
    model = StalkWeek

    def get_queryset(self):
        return StalkWeek.objects.order_by('sunday')


class StalkWeekDetail(generic.DetailView):
    template_name = 'stalks/stalk_week_detail.html'
    model = StalkWeek


class Prefix:
    STALK_WEEK = 'stalk-week'

    @staticmethod
    def turnip_stacks(i): return f'turnip-stacks{i}'

    @staticmethod
    def day_prices(i): return f'day-price{i}'


def get_all_turnip_stacks(post):
    ret_list = []
    i = 0
    prefix = Prefix.turnip_stacks(i)
    while True:
        turnip_stacks_form = AddTurnipStacksForm(post, prefix=prefix)
        if not turnip_stacks_form.is_valid():
            break
        ret_list.append(turnip_stacks_form)
        i += 1
        prefix = Prefix.turnip_stacks(i)
    return ret_list


def get_all_day_prices(post):
    ret_list = []
    i = 0
    prefix = Prefix.day_prices(i)
    while True:
        day_price_form = AddDayPriceForm(post, prefix=prefix)
        if not day_price_form.is_valid():
            break
        ret_list.append(day_price_form)
        i += 1
        prefix = Prefix.day_prices(i)
    return ret_list


def add_stalk_week(request):
    if request.method == 'POST':
        stalk_week = AddStalkWeekForm(request.POST, prefix='stalk-week')
        turnip_stacks_form_list = get_all_turnip_stacks(request.POST)
        day_price_form_list = get_all_day_prices(request.POST)
        if stalk_week.is_valid():
            new_stalk_week = stalk_week.save()
            for stack in turnip_stacks_form_list:
                stack.save(new_stalk_week.id)
            for day_price in day_price_form_list:
                day_price.save(new_stalk_week.id)
    else:
        stalk_week = AddStalkWeekForm(prefix='stalk-week')
        turnip_stacks_form_list = [AddTurnipStacksForm(prefix='turnip-stacks0')]
        day_price_form_list = [AddDayPriceForm(prefix='day-price0')]
    return render(
        request,
        'stalks/stalk_week_form.html',
        {
            'stalk_week': stalk_week,
            'turnip_stacks_form_list': turnip_stacks_form_list,
            'day_price_form_list': day_price_form_list,
        },
    )


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


# def sell_turnip_stacks(request, stalk_week_id):
#     if request.method == 'POST':
#         form = SellTurnipStacksForm(request.POST, stalk_week_id=stalk_week_id)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('stalks:stalk_week_detail', args=(stalk_week_id,)))
#     else:
#         form = SellTurnipStacksForm(initial={'sell_date': timezone.now()})
#     stalk_week = get_object_or_404(StalkWeek, pk=stalk_week_id)
#     return render(request, 'stalks/sell_turnip_stacks_form.html', {'stalk_week': stalk_week, 'form': form})


def delete_stalk_week(response, pk):
    stalk_week = get_object_or_404(StalkWeek, pk=pk)
    affected = stalk_week.delete()
    return HttpResponseRedirect(reverse('stalks:stalk_week_lists'))


def validate_stalk_week(request):
    json_reply = {}
    current_date = request.POST.get('current_date')
    buy_price = int(request.POST.get('buy_price'))
    turnip_stacks = int(request.POST.get('turnip_stacks'))
    if current_date:
        sunday = DateHelper(current_date, '%B %d %Y').sunday()
        if StalkWeek.objects.filter(sunday=sunday).first():
            json_reply['current_date'] = 'Error: A stalk week is already created for this week'
    if buy_price < 90 or buy_price > 110:
        json_reply['buy_price'] = 'Error: Buy price must be between 90 and 110'
    if turnip_stacks < 0:
        json_reply['turnip_stacks'] = 'Error: Turnip stacks must be 0 or a positive number'
    return JsonResponse(json_reply)

