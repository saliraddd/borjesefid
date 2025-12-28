from django import template

register = template.Library()

@register.filter
def div(value, arg):
    """
    تقسیم value بر arg
    مثلاً {{ price|div:10 }} برای تبدیل ریال به تومان
    """
    try:
        return int(value) // int(arg)
    except (ValueError, ZeroDivisionError):
        return 0
    
