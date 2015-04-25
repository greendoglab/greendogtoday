from django.shortcuts import render, get_object_or_404
from django.db.models import F
from blog.models import Post, Tag


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
    context = {
        'post': get_object_or_404(Tag, slug=slug)
    }
    return render(request, template, context)
