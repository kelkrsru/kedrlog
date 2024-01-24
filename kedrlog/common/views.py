import re


def get_clean_phone(phone_number):
    """Метод для очистки телефонного номера от всех символов, кроме цифр"""
    return ''.join(re.findall(r'\d+', phone_number))
