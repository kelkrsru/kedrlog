from core.models import Company
from django.shortcuts import get_object_or_404, render
from staticpages.models import (ContentPrice, ContentSpa, GalleryFood,
                                GalleryHouses, GalleryTerritory,
                                TextContentAccessories, TextContentCorporate,
                                TextContentFz152, TextContentRent,
                                TextContentRules)


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
    return render(request, template, context)


def page_text_content(request):
    """Метод страницы с текстовым контентом."""
    template = 'staticpages/page_text_content.html'

    page = request.resolver_match.url_name

    company = Company.objects.get(active=True)
    if page == 'rules':
        text_content = get_object_or_404(TextContentRules, active=True)
    elif page == 'fz152':
        text_content = get_object_or_404(TextContentFz152, active=True)
    elif page == 'accessories':
        text_content = get_object_or_404(TextContentAccessories, active=True)
    elif page == 'rent':
        text_content = get_object_or_404(TextContentRent, active=True)
    elif page == 'corporate':
        text_content = get_object_or_404(TextContentCorporate, active=True)
    else:
        text_content = None

    context = {
        'company': company,
        'text_content': text_content
    }
    return render(request, template, context)


def page_price(request):
    """Метод страницы с ценами."""
    template = 'staticpages/price.html'

    price_content = get_object_or_404(ContentPrice, active=True)
    company = Company.objects.get(active=True)

    context = {
        'company': company,
        'price_content': price_content
    }
    return render(request, template, context)


def page_spa(request):
    """Метод страницы с ценами."""
    template = 'staticpages/spa.html'

    spa_content = get_object_or_404(ContentSpa, active=True)
    company = Company.objects.get(active=True)

    context = {
        'company': company,
        'spa_content': spa_content
    }
    return render(request, template, context)
