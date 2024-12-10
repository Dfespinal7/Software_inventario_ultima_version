from django import template

register = template.Library()

@register.filter
def format_currency(value):
    try:
        # Intenta formatear el valor como un número y separarlo por miles
        return "{:,.0f}".format(float(value)).replace(',', '.')
    except (ValueError, TypeError):
        return value
