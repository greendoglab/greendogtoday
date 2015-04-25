from django import template
from pages.models import Page

register = template.Library()


@register.inclusion_tag('templatetags/pages_menu.html')
def show_pages_menu():
    return {
        'items': Page.objects.filter(in_menu=True),
    }
