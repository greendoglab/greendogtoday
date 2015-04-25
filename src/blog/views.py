# -*-coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.db.models import F
from blog.models import Post, Tag
from accounts.models import Account


def post(request, slug):
    template = 'post.html'
    Post.objects.filter(slug=slug).update(views=F('views') + 1)
    related_posts = Post.objects.exclude(slug=slug).order_by('?')[:4]
    context = {
        'post': get_object_or_404(Post, slug=slug),
        'related_posts': related_posts
    }
    return render(request, template, context)


def tag(request, slug):
    template = 'tag.html'
    tag = get_object_or_404(Tag, slug=slug)
    context = {
        'tag': tag,
        'posts': Post.objects.filter(tags__name__in=[tag])
    }
    return render(request, template, context)


def author(request, slug):
    template = 'author.html'

    author = Account.objects.get(slug=slug)
    posts = Post.objects.filter(author=author)

    context = {
        'posts': posts,
        'author': author
    }
    return render(request, template, context)
