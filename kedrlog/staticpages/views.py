from django.shortcuts import render, get_object_or_404

from core.models import Company
from staticpages.models import GalleryHouses, GalleryTerritory, GalleryFood, TextContentRules, TextContentAccessories, \
    TextContentRent


def page_gallery(request):
    """Метод страницы галереи."""
    template = 'staticpages/page_gallery.html'

    page = request.resolver_match.url_name

    company = Company.objects.get(active=True)
    if page == 'houses':
        gallery = get_object_or_404(GalleryHouses, active=True)
    elif page == 'territory':
        gallery = get_object_or_404(GalleryTerritory, active=True)
    elif page == 'food':
        gallery = get_object_or_404(GalleryFood, active=True)
    else:
        gallery = None

    context = {
        'company': company,
        'gallery': gallery
    }
    response = render(request, template, context)
    return response


def page_text_content(request):
    """Метод страницы с текстовым контентом."""
    template = 'staticpages/page_text_content.html'

    page = request.resolver_match.url_name

    company = Company.objects.get(active=True)
    if page == 'rules':
        text_content = get_object_or_404(TextContentRules, active=True)
    elif page == 'accessories':
        text_content = get_object_or_404(TextContentAccessories, active=True)
    elif page == 'rent':
        text_content = get_object_or_404(TextContentRent, active=True)
    else:
        text_content = None

    context = {
        'company': company,
        'text_content': text_content
    }
    response = render(request, template, context)
    return response
