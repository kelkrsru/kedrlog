import re

from bitrix24 import Bitrix24, BitrixError
from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone

from common.views import get_clean_phone, user_get_or_create_in_site, contact_get_or_create_in_b24
from core.models import OrderGiftCertificate, GiftCertificate, SettingsBitrix24

User = get_user_model()


class OrderGiftCertificateForm(BSModalModelForm):

    def __init__(self, *args, **kwargs):

        super(OrderGiftCertificateForm, self).__init__(*args, **kwargs)
        gift_cert_id = self.initial.get('gift_cert_id')
        self.gift_certificate = GiftCertificate.objects.get(pk=gift_cert_id)

        self.fields['user_name'].label = 'Ваше имя:'
        self.fields['user_name'].help_text = None
        self.fields['user_name'].required = True

        self.fields['user_lastname'].label = 'Ваша фамилия:'
        self.fields['user_lastname'].help_text = None
        self.fields['user_lastname'].required = True

        self.fields['user_phone'].label = 'Ваш номер телефона:'
        self.fields['user_phone'].help_text = None
        self.fields['user_phone'].required = True
        self.fields['user_phone'].widget = forms.TextInput(attrs={'data-phone-pattern': True})

        self.fields['user_email'].label = 'Ваш адрес электронной почты:'
        self.fields['user_email'].help_text = None
        self.fields['user_email'].required = True

        self.fields['user_address'].label = 'Укажите адрес доставки сертификата'
        self.fields['user_address'].help_text = None
        self.fields['user_address'].required = True
        self.fields['user_address'].widget = forms.HiddenInput(attrs={'value': 'address'})

        self.fields['type'].label = 'Выберите тип вашего сертификата (способ доставки):'
        self.fields['type'].help_text = None
        self.fields['type'].empty_label = 'Не выбрано'
        self.fields['type'].queryset = self.gift_certificate.type.all()

        self.fields['price'].label = 'Выберите сумму вашего сертификата:'
        self.fields['price'].help_text = None
        self.fields['price'].widget = forms.NumberInput(attrs={'step': self.gift_certificate.step_price,
                                                               'max': self.gift_certificate.max_price,
                                                               'min': self.gift_certificate.min_price,
                                                               'value': self.gift_certificate.min_price})

        self.user = self.initial.get('user') or None
        if self.user:
            self.initial['user_name'] = self.user.first_name
            self.initial['user_lastname'] = self.user.last_name
            self.initial['user_email'] = self.user.email
            self.initial['user_phone'] = self.user.phone
            self.fields['user_phone'].widget.attrs['disabled'] = True
            self.fields['user_phone'].help_text = f'Для изменения номера телефона необходимо отредактировать свойства вашего пользователя в <a href="{reverse_lazy("personal:index")}">личном кабинете</a>'
            self.initial['user_name'] = self.user.first_name

    def save(self, commit=True):
        data = self.cleaned_data
        settings = SettingsBitrix24.objects.get(active=True)

        # Проверяем пользователя на сайте
        if not self.user or not self.user.is_authenticated:
            self.user = user_get_or_create_in_site(data.get('user_phone'), data.get('user_email'),
                                                   data.get('user_name'), data.get('user_lastname'))

        # Проверяем пользователя в Битрикс24
        webhook = SettingsBitrix24.objects.get(active=True).webhook
        b24 = Bitrix24(webhook)
        if self.user.id_b24:
            try:
                contact = b24.callMethod('crm.contact.get', id=self.user.id_b24)
            except BitrixError:
                contact = contact_get_or_create_in_b24(b24, self.user, settings.responsible_by_default)
        else:
            contact = contact_get_or_create_in_b24(b24, self.user, settings.responsible_by_default)

        # Рассчитываем срок действия срок действия
        validity_date_time = (timezone.now() + timezone.timedelta(days=self.gift_certificate.validity)
                              if self.gift_certificate.validity else None)

        order = super(OrderGiftCertificateForm, self).save(commit=False)
        order.user = self.user
        order.gift_certificate = self.gift_certificate
        order.validity_date_time = validity_date_time

        if not commit:
            return order

        order.save()

        # Отправка информации о сертификате администратору
        if order.gift_certificate.send_email:
            subject = 'Заказ подарочного сертификата на сайте https://kedrlog.ru'
            message = render_to_string('staticpages/order_gift_cert_created_email.html', {
                'user': self.user,
                'certificate': order
            })
            from_email = None
            recipient_list = [order.gift_certificate.email]
            send_mail(subject, message, from_email, recipient_list)

        return order

    class Meta:
        model = OrderGiftCertificate
        fields = ['user_name', 'user_lastname', 'user_address', 'user_phone', 'user_email', 'type', 'price']
