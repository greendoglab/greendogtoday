# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from utils import *


class Page(models.Model):
    poster = models.CharField('Poster', max_length=1000, help_text='Image url', blank=True)
    slug = models.SlugField('Link', unique=True, max_length=255, help_text='Link', blank=True)
    title = models.CharField('Title', max_length=255, help_text='Something goes here')
    content = models.TextField('Content', help_text='Work content Markdown')
    in_menu = models.BooleanField('In menu', default=False,)
    POST_STATUS = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    status = models.CharField('Post status', max_length=20, choices=POST_STATUS, default='draft')

    def __unicode__(self):
        return self.title

    def get_poster(self):
        return MakeImage(self.image, settings.POSTER_THUMBS_SIZE, crop='center')

    def get_mobile_poster(self):
        return MakeImage(self.image, settings.POSTER_SMALL_THUMBS_SIZE, crop='center')

    def get_squae_poster(self):
        return MakeImage(self.image, settings.SQUARE_THUMBS_SIZE, crop='center')

    def get_content(self):
        return MakeContent(self.content)

    def get_url(self):
        return reverse('page', args=(self.slug,))

    class Meta:
        ordering = ['-pk']
        verbose_name_plural = "Page"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = MakeSlug(self.title)
        super(Page, self).save(*args, **kwargs)
