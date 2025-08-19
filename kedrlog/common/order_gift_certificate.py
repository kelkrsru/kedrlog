from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string

from bitrix24 import Bitrix24, BitrixError
from common.views import contact_get_or_create_in_b24, user_get_or_create_in_site
from core.models import SettingsBitrix24


class GiftCertificateOrderService:
    def __init__(self, order, user, gift_certificate):
        self.order = order
        self.user = user
        self.gift_certificate = gift_certificate
        self.settings = SettingsBitrix24.objects.get(active=True)
        self.b24 = Bitrix24(self.settings.webhook)

    # --- Шаг 1: работа с пользователем ---
    def get_or_create_user(self):
        if not self.user or not self.user.is_authenticated:
            self.user = user_get_or_create_in_site(
                self.order.user_phone,
                self.order.user_email,
                self.order.user_name,
                self.order.user_lastname,
            )
        return self.user

    # --- Шаг 2: синхронизация с Bitrix24 ---
    def sync_with_bitrix(self):
        if self.user.id_b24:
            try:
                self.b24.callMethod("crm.contact.get", id=self.user.id_b24)
            except BitrixError:
                contact_get_or_create_in_b24(self.b24, self.user, self.settings.responsible_by_default)
        else:
            contact_get_or_create_in_b24(self.b24, self.user, self.settings.responsible_by_default)

    # --- Шаг 3: срок действия ---
    def set_validity_date(self):
        if self.gift_certificate.validity:
            self.order.validity_date_time = timezone.now() + timezone.timedelta(
                days=self.gift_certificate.validity
            )

    # --- Шаг 4: сохранение заказа ---
    def save_order(self):
        self.order.user = self.user
        self.order.gift_certificate = self.gift_certificate
        self.order.save()
        return self.order

    # --- Шаг 5: отправка email ---
    def notify_admin(self):
        if self.gift_certificate.send_email:
            subject = "Заказ подарочного сертификата на сайте https://kedrlog.ru"
            message = render_to_string(
                "staticpages/order_gift_cert_created_email.html",
                {"user": self.user, "certificate": self.order},
            )
            send_mail(subject, "", None, [self.gift_certificate.email], html_message=message)

    # --- orchestration ---
    def process(self):
        self.get_or_create_user()
        self.sync_with_bitrix()
        self.set_validity_date()
        self.save_order()
        self.notify_admin()
        return self.order
