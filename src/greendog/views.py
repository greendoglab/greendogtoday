# -*-coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from itertools import chain
from django.contrib.syndication.views import Feed
from django.conf import settings
from blog.models import Post


def HomeView(request):
    template = 'index.html'

    context = {
        'posts': Post.objects.all(),
    }
    return render(request, template, context)


def SearchView(request):
    template_name = 'search_results.html'

    q = request.GET.get('q', None)
    if q is None or q == '':
        return redirect('/')

    object_list = []

    query = (Q(title__istartswith=q) | Q(title__icontains=q) |
             Q(content__istartswith=q) | Q(content__icontains=q))

    models = ContentType.objects.filter(
        model__in=settings.SEARCHABLE_OBJECTS).all()
    for model in models:
        obj = model.get_all_objects_for_this_type().filter(query).all()
        object_list = chain(object_list, obj)

    objects = list(object_list)

    context = {'objects': objects, 'q': q}
    template = template_name
    return render(request, template, context)


class AllFeed(Feed):
    title = u"title"
    link = "/"
    description = "Путешествия"

    def items(self):
        return Post.objects.all()[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.get_content()
