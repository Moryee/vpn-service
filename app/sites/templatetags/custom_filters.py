from django import template


register = template.Library()


@register.filter
def divide(value, arg):
    try:
        return round(int(value) / int(arg), 3)
    except ZeroDivisionError:
        return 0
    except ValueError:
        return None
