from django import template
from blog.models import Post

register = template.Library()


@register.inclusion_tag('templatetags/popular.html')
def show_popular():
    return {
        'items': Post.objects.order_by('-views')[:5],
    }
