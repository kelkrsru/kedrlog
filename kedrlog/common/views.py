import re

from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

User = get_user_model()


# ******************************************* Users methods ***********************************************************
def get_clean_phone(phone_number):
    """Метод для очистки телефонного номера от всех символов, кроме цифр"""
    return ''.join(re.findall(r'\d+', phone_number))


def user_get_or_create_in_site(user_phone, user_email, user_first_name, user_last_name):
    """Метод, который проверяет пользователя на сайте и создает в случаи отсутствия"""

    user_phone_clear = get_clean_phone(user_phone)
    user, created = User.objects.get_or_create(
        phone=user_phone, defaults={'username': user_phone_clear, 'email': user_email,
                                    'first_name': user_first_name, 'last_name': user_last_name})
    if created:
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()
        subject = 'Activate your account'
        message = render_to_string('order/user_create_email.html', {
            'user': user,
            'password': password
        })
        user.email_user(subject, message)
    return user


def contact_get_or_create_in_b24(b24, user, responsible):
    """Метод получения контакта в Б24, а в случаи отсутствия контакта, он его создает в Б24."""

    user_phone_clear = get_clean_phone(user.phone)
    contacts = b24.callMethod('crm.duplicate.findbycomm', entity_type="CONTACT", type="PHONE",
                              values=[user_phone_clear])
    if not contacts:
        fields = {
            'NAME': user.first_name,
            'LAST_NAME': user.last_name,
            'OPENED': 'Y',
            'ASSIGNED_BY_ID': responsible,
            'TYPE_ID': 'CLIENT',
            'PHONE': [{'VALUE': user_phone_clear, 'VALUE_TYPE': 'WORK'}],
            'EMAIL': [{'VALUE': user.email, 'VALUE_TYPE': 'WORK'}],
        }
        contact_id = b24.callMethod('crm.contact.add', fields=fields)
    else:
        contact_id = contacts.get('CONTACT')[0]
    user.id_b24 = contact_id
    user.save()
    return b24.callMethod('crm.contact.get', id=user.id_b24)
# **********************************************************************************************************************
