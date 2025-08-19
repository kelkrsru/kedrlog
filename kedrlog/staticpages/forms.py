import phonenumbers

from django import forms
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from bootstrap_modal_forms.forms import BSModalModelForm

from core.models import OrderGiftCertificate, GiftCertificate
from common.order_gift_certificate import GiftCertificateOrderService


class OrderGiftCertificateForm(BSModalModelForm):
    FIELD_CONFIG = {
        "user_name": {"label": "Ваше имя:", "required": True},
        "user_lastname": {"label": "Ваша фамилия:", "required": True},
        "user_phone": {
            "label": "Ваш номер телефона:",
            "required": True,
            "widget": forms.TextInput(attrs={"data-phone-pattern": True}),
        },
        "user_email": {"label": "Ваш адрес электронной почты:", "required": True},
        "user_address": {
            "label": "Укажите адрес доставки сертификата",
            "required": True,
            "widget": forms.HiddenInput(attrs={"value": "address"}),
        },
    }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        gift_cert_id = kwargs.get("initial", {}).get("gift_cert_id")
        super().__init__(*args, **kwargs)

        self.gift_certificate = GiftCertificate.objects.get(pk=gift_cert_id)

        # Настройка полей по словарю
        for field_name, cfg in self.FIELD_CONFIG.items():
            f = self.fields[field_name]
            f.label = cfg["label"]
            f.help_text = None
            f.required = cfg.get("required", False)
            if "widget" in cfg:
                f.widget = cfg["widget"]

        # Поля type и price зависят от сертификата
        self.fields["type"].label = "Выберите тип вашего сертификата (способ доставки):"
        self.fields["type"].help_text = None
        self.fields["type"].empty_label = "Не выбрано"
        self.fields["type"].queryset = self.gift_certificate.type.all()

        self.fields["price"].label = "Выберите сумму вашего сертификата:"
        self.fields["price"].help_text = None
        self.fields["price"].widget = forms.NumberInput(
            attrs={
                "step": self.gift_certificate.step_price,
                "max": self.gift_certificate.max_price,
                "min": self.gift_certificate.min_price,
                "value": self.gift_certificate.min_price,
            }
        )

        # Если пользователь передан
        if self.user:
            self.initial.setdefault("user_name", self.user.first_name)
            self.initial.setdefault("user_lastname", self.user.last_name)
            self.initial.setdefault("user_email", self.user.email)
            self.initial.setdefault("user_phone", self.user.phone)
            self.fields["user_phone"].widget.attrs["readonly"] = True
            self.fields["user_phone"].help_text = (
                f'Для изменения номера телефона необходимо отредактировать свойства '
                f'вашего пользователя в <a href="{reverse_lazy("personal:index")}">'
                f'личном кабинете</a>'
            )

    def clean_user_phone(self):
        phone = self.cleaned_data.get("user_phone")

        if not phone:
            raise ValidationError("Номер телефона обязателен.")

        try:
            parsed_phone = phonenumbers.parse(phone, "RU")  # RU как дефолтная страна
        except phonenumbers.NumberParseException:
            raise ValidationError("Некорректный номер телефона.")

        if not phonenumbers.is_valid_number(parsed_phone):
            raise ValidationError("Введите правильный номер телефона.")

        # Форматируем в международный формат (E.164)
        normalized = phonenumbers.format_number(
            parsed_phone, phonenumbers.PhoneNumberFormat.E164
        )
        # убираем "+"
        return normalized.lstrip("+")

    def save(self, commit=True):
        order = super().save(commit=False)
        if commit:
            service = GiftCertificateOrderService(order, self.user, self.gift_certificate)
            order = service.process()
        return order

    class Meta:
        model = OrderGiftCertificate
        fields = [
            "user_name",
            "user_lastname",
            "user_address",
            "user_phone",
            "user_email",
            "type",
            "price",
        ]
