# -*-coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings
from utils import *

SQUARE_THUMBS_SIZE = "240x240"


class Profile(models.Model):
    user = models.OneToOneField(User)
    photo = models.CharField('Poster', max_length=1000, help_text='Image url', blank=True)
    slug = models.SlugField('Link', unique=True, max_length=255, help_text='Link', blank=True)
    name = models.CharField('Title', max_length=255, help_text='Something goes here')

    def get_photo(self):
        return MakeImage(self.photo, settings.SQUARE_THUMBS_SIZE, crop='center')

    def get_url(self):
        return reverse('author', args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = MakeSlug(self.name)
        super(Profile, self).save(*args, **kwargs)
