# -*-coding: utf-8 -*-
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from endless_pagination.decorators import page_template
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from itertools import chain
from django.contrib.syndication.views import Feed
from django.conf import settings
from django.core.urlresolvers import reverse
from blog.models import Post


@page_template('posts_template.html')
def HomeView(
        request,
        template='index.html',
        extra_context=None):

    context = {
        'posts': Post.objects.all().filter(status="published")
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))


@page_template('posts_template.html')
def SearchView(request, template='search_results.html', extra_context=None):

    q = request.GET.get('q', None)
    if q is None or q == '':
        return redirect('/')

    object_list = []

    query = (Q(title__istartswith=q) | Q(title__icontains=q) |
             Q(content__istartswith=q) | Q(content__icontains=q))

    models = ContentType.objects.filter(
        model__in=settings.SEARCHABLE_OBJECTS).filter(status="published")
    for model in models:
        obj = model.get_all_objects_for_this_type().filter(query).filter(status="published")
        object_list = chain(object_list, obj)

    objects = list(object_list)

    context = {
        'posts': objects,
        'q': q
    }

    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))


class AllFeed(Feed):
    title = u"title"
    link = "/"
    description = "Путешествия"

    def items(self):
        return Post.objects.filter(status="published")[:10]

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return reverse('post', args=[item.slug])

    def item_description(self, item):
        return item.get_content()
