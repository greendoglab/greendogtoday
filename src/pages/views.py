from django.shortcuts import render, get_object_or_404
from pages.models import Page


def page(request, slug):
    template = 'page.html'

    context = {
        'post': get_object_or_404(Page, slug=slug)
    }
    return render(request, template, context)
