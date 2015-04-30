# -*-coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import text
from utils import *
import re
import datetime


class Tag(models.Model):
    poster = models.CharField('Poster', max_length=1000, help_text='Image url', blank=True)
    slug = models.SlugField('Link', unique=True, max_length=255, help_text='Link', blank=True)
    title = models.CharField('Title', max_length=255, help_text='Something goes here')
    content = models.TextField('Content', help_text='Markdown', blank=True)

    def __unicode__(self):
        return self.title

    def get_poster(self):
        return MakeImage(self.poster, settings.POSTER_THUMBS_SIZE, crop='center')

    def get_mobile_poster(self):
        return MakeImage(self.poster, settings.POSTER_SMALL_THUMBS_SIZE, crop='center')

    def get_squae_poster(self):
        return MakeImage(self.poster, settings.SQUARE_THUMBS_SIZE, crop='center')

    def get_content(self):
        return MakeContent(self.content)

    def get_url(self):
        return reverse('tag', args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = MakeSlug(self.title)
        super(Tag, self).save(*args, **kwargs)


class Post(models.Model):
    poster = models.CharField('Poster', max_length=1000, help_text='Image url', blank=True)
    slug = models.SlugField('Link', unique=True, max_length=255, help_text='Link', blank=True)
    date = models.DateTimeField('Date', default=datetime.datetime.now)
    title = models.CharField('Title', max_length=255, help_text='Something goes here')
    content = models.TextField('Content', help_text='Work content Markdown')
    tags = models.ManyToManyField('Tag', related_name='Tag', blank=True)

    POST_STATUS = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    status = models.CharField('Post status', max_length=20, choices=POST_STATUS, default='draft')

    views = models.PositiveIntegerField(default=0)

    author = models.ForeignKey(User, null=True, blank=True)

    def __unicode__(self):
        return self.title

    def get_poster(self):
        return MakeImage(self.poster, settings.POSTER_THUMBS_SIZE, crop='center')

    def get_mobile_poster(self):
        return MakeImage(self.poster, settings.POSTER_SMALL_THUMBS_SIZE, crop='center')

    def get_squae_poster(self):
        return MakeImage(self.poster, settings.SQUARE_THUMBS_SIZE, crop='center')

    def get_short_content(self):
        content = MakeContent(self.content)
        content = re.sub('<[^>]*>', '', content)
        content = re.sub(r'<img.*?/>', '', content)
        return text.Truncator(content).words(40, html=True, truncate=' ...')

    def get_content(self):
        return MakeContent(self.content)

    def get_url(self):
        return reverse('post', args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = MakeSlug(self.title)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Post'
