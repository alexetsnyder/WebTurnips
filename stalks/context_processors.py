from .models import StalkWeek


def navbar_context(request):
    return {'navbar_stalk_week_list': StalkWeek.objects.order_by("sunday")[:10]}
