from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from core.models import Company, Reserve


@login_required
def index(request):
    """Метод главной страницы."""
    template = 'personal/index.html'

    company = Company.objects.get(active=True)

    context = {
        'company': company,
    }
    response = render(request, template, context)
    return response


@login_required
def reserve(request):
    """Метод раздела Бронирования."""
    template = 'personal/reserve.html'

    company = Company.objects.get(active=True)

    dt_now = timezone.now().replace(tzinfo=timezone.get_current_timezone())
    reserves = Reserve.objects.filter(end_date_time__gte=dt_now, user=request.user)

    context = {
        'company': company,
        'reserves': reserves
    }
    response = render(request, template, context)
    return response


@login_required
def bonus(request):
    """Метод раздела Бонусы."""
    template = 'personal/bonus.html'

    company = Company.objects.get(active=True)

    context = {
        'company': company,
    }
    response = render(request, template, context)
    return response
