# my_aegbp/templatetags/form_tags.py

from django import template

register = template.Library()

@register.filter
def get_field(form, field_name):
    return form[field_name]
