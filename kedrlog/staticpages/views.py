from bootstrap_modal_forms.generic import BSModalCreateView
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView

from core.models import Company, GiftCertificate, OrderGiftCertificate, SettingsSite
from django.shortcuts import get_object_or_404, render
import staticpages.models as static_pages_models
from staticpages.forms import OrderGiftCertificateForm

User = get_user_model()
COMPANY = Company.objects.get(active=True)


def page_gallery(request):
    """Метод страницы галереи."""
    template = 'staticpages/page_gallery.html'

    page = request.resolver_match.url_name

    if page == 'houses':
        gallery = get_object_or_404(static_pages_models.GalleryHouses, active=True)
    elif page == 'territory':
        gallery = get_object_or_404(static_pages_models.GalleryTerritory, active=True)
    elif page == 'food':
        gallery = get_object_or_404(static_pages_models.GalleryFood, active=True)
    else:
        gallery = None

    context = {
        'company': COMPANY,
        'gallery': gallery
    }
    return render(request, template, context)


def page_text_content(request):
    """Метод страницы с текстовым контентом."""
    template = 'staticpages/page_text_content.html'

    page = request.resolver_match.url_name

    if page == 'rules':
        text_content = get_object_or_404(static_pages_models.TextContentRules, active=True)
    elif page == 'fz152':
        text_content = get_object_or_404(static_pages_models.TextContentFz152, active=True)
    elif page == 'accessories':
        text_content = get_object_or_404(static_pages_models.TextContentAccessories, active=True)
    elif page == 'rent':
        text_content = get_object_or_404(static_pages_models.TextContentRent, active=True)
    elif page == 'corporate':
        text_content = get_object_or_404(static_pages_models.TextContentCorporate, active=True)
    elif page == 'rules-gift-cert':
        text_content = get_object_or_404(static_pages_models.TextContentRulesGiftCert, active=True)
    else:
        text_content = None

    context = {
        'company': COMPANY,
        'text_content': text_content
    }
    return render(request, template, context)


def page_price(request):
    """Метод страницы с ценами."""
    template = 'staticpages/price.html'

    price_content = get_object_or_404(static_pages_models.ContentPrice, active=True)

    context = {
        'company': COMPANY,
        'price_content': price_content
    }
    return render(request, template, context)


def page_spa(request):
    """Метод страницы с ценами."""
    template = 'staticpages/spa.html'

    spa_content = get_object_or_404(static_pages_models.ContentSpa, active=True)

    context = {
        'company': COMPANY,
        'spa_content': spa_content,
        'spa_services': spa_content.spa_service.all().order_by('sort', 'pk')
    }
    return render(request, template, context)


def page_gift_certificate(request):
    """Метод страницы Подарочные сертификаты."""
    template = 'staticpages/gift_certificate.html'

    gift_certificate_content = get_object_or_404(static_pages_models.ContentGiftCertificate, active=True)
    context = {
        'company': COMPANY,
        'gift_certificate_content': gift_certificate_content,
        'one_cert': False
    }
    # Заглушка для простых пользователей
    settings_site = get_object_or_404(SettingsSite, active=True)
    context_closed = {'company': COMPANY, 'text': settings_site.text_gift_certificate_closed}
    if settings_site.gift_certificate_closed_all and not request.user.is_superuser:
        return render(request, 'staticpages/gift_certificate_closed.html', context_closed)
    if settings_site.gift_certificate_closed and not request.user.is_superuser and not request.user.is_staff:
        return render(request, 'staticpages/gift_certificate_closed.html', context_closed)

    if gift_certificate_content.gift_certificates.count() == 1:
        gift_cert = gift_certificate_content.gift_certificates.first()
        user = None
        if request.user.is_authenticated:
            user = request.user
        form = OrderGiftCertificateForm(request.POST or None, initial={'gift_cert_id': gift_cert.pk, 'user': user},
                                        request=request)

        context['one_cert'] = True
        context['form'] = form
        context['certificate'] = gift_cert

        if form.is_valid():
            order = form.save()
            return HttpResponseRedirect(reverse_lazy('ok-cert', kwargs={'pk': order.pk}))

    return render(request, template, context)


class OrderGiftCertificateCreateView(BSModalCreateView):
    template_name = 'staticpages/gift_certificate_form.html'
    form_class = OrderGiftCertificateForm
    gift_cert_id = None

    def get_initial(self):
        initial = super(OrderGiftCertificateCreateView, self).get_initial()
        self.gift_cert_id = self.kwargs.get('gift_cert_id', None)
        initial['gift_cert_id'] = self.gift_cert_id
        if self.request.user.is_authenticated:
            initial['user'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        data = super(OrderGiftCertificateCreateView, self).get_context_data(**kwargs)
        data['certificate'] = GiftCertificate.objects.get(pk=self.gift_cert_id)
        return data

    # Здесь костыль
    def get_success_url(self):
        cert = OrderGiftCertificate.objects.last()
        return reverse_lazy('ok-cert', kwargs={'pk': cert.pk})


class OrderGiftCertificateDetailView(DetailView):
    template_name = 'staticpages/gift_certificate_ok.html'
    model = OrderGiftCertificate

    def get_context_data(self, **kwargs):
        context = super(OrderGiftCertificateDetailView, self).get_context_data(**kwargs)
        settings_site = get_object_or_404(SettingsSite, active=True)
        context['company'] = COMPANY
        context['text'] = settings_site.text_gift_certificate_ok
        return context
