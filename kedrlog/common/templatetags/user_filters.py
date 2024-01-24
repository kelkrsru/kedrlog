import decimal
import re

from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


# Возврат типа виджета
@register.filter
def widgettype(field):
    return field.field.widget.__class__.__name__


@register.filter
def fieldtype(field):
    return field.field.widget.__class__.__name__


@register.filter
def emptyvalue(field):
    if not field:
        return 0
    return field


@register.filter
def clear_phone(value):
    return ''.join(re.findall(r'\d+', value))


@register.filter
def to_int(value):
    return int(value)


@register.filter
def distinct(queryset, field_name):
    return queryset.values(field_name).distinct()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def equal_date(date_one, date_two):
    return date_one <= date_two


@register.simple_tag
def multiply(qty, unit_price):
    return round(decimal.Decimal(qty) * decimal.Decimal(unit_price), 2)


@register.simple_tag
def tax_sum(qty, unit_price, rate):
    sum = decimal.Decimal(qty) * decimal.Decimal(unit_price)
    return round(sum * decimal.Decimal(rate) / 100, 2)


register.filter('addclass', addclass)
register.filter('fieldtype', fieldtype)
register.filter('emptyvalue', emptyvalue)
