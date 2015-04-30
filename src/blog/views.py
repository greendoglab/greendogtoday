# -*-coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from endless_pagination.decorators import page_template
from django.db.models import F
from blog.models import Post, Tag
from profiles.models import Profile


def post(request, slug):

    template = 'post.html'
    Post.objects.filter(slug=slug).update(views=F('views') + 1)
    related_posts = Post.objects.exclude(slug=slug).order_by('?')[:4]
    context = {
        'post': get_object_or_404(Post, slug=slug),
        'related_posts': related_posts
    }
    return render(request, template, context)


@page_template('posts_template.html')
def tag(request, slug, template='tag.html', extra_context=None):

    tag = get_object_or_404(Tag, slug=slug)
    context = {
        'tag': tag,
        'posts': Post.objects.filter(tags=tag).filter(status="published")
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))


@page_template('posts_template.html')
def author(request, slug, template='author.html', extra_context=None):

    author = Profile.objects.get(slug=slug)
    author_user = author.user
    posts = Post.objects.filter(author=author_user).filter(status="published")
    context = {
        'posts': posts,
        'author': author
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))
