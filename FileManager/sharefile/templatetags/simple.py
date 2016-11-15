
from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def error_msg(error_list):
    if(error_list):
        return error_list[0]
    return ""