from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import StalkWeek


class IndexView(generic.ListView):
    template_name = 'stalks/index.html'
    model = StalkWeek


class StalkWeekDetail(generic.DetailView):
    template_name = 'stalks/stalk_week_detail.html'
    model = StalkWeek
