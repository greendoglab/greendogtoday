""" User models."""
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from utils import *


class AccountManager(BaseUserManager):

    """ Custom manager for EmailUser."""

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """ Create and save an EmailUser with the given email and password.

        :param str email: user email
        :param str password: user password
        :param bool is_staff: whether user staff or not
        :param bool is_superuser: whether user admin or not
        :return custom_user.models.EmailUser user: user
        :raise ValueError: email is not set

        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        is_active = extra_fields.pop("is_active", True)
        user = self.model(email=email, is_staff=is_staff, is_active=is_active,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """ Create and save an EmailUser with the given email and password.

        :param str email: user email
        :param str password: user password
        :return custom_user.models.EmailUser user: regular user

        """
        is_staff = extra_fields.pop("is_staff", False)
        return self._create_user(email, password, is_staff, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """ Create and save an EmailUser with the given email and password.

        :param str email: user email
        :param str password: user password
        :return custom_user.models.EmailUser user: admin user

        """
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class AbstractAccount(AbstractBaseUser, PermissionsMixin):

    """ Abstract User with the same behaviour as Django's default User.

    AbstractEmailUser does not have username field. Uses email as the
    USERNAME_FIELD for authentication.

    Use this if you need to extend EmailUser.

    Inherits from both the AbstractBaseUser and PermissionMixin.

    The following attributes are inherited from the superclasses:
        * password
        * last_login
        * is_superuser

    """

    email = models.EmailField(_('email address'), max_length=255,
                              unique=True, db_index=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False, help_text=_(
            'Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_(
        'Designates whether this user should be treated as '
        'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    name = models.CharField(max_length=300)
    photo = models.CharField(max_length=1000, help_text="Photo: URL", blank=True)
    poster = models.CharField(max_length=1000, help_text="Poster: URL", blank=True)
    twitter = models.CharField(max_length=300, help_text="nickname", blank=True)
    instagram = models.CharField(max_length=300, help_text="nickname", blank=True)
    facebook = models.CharField(max_length=500, help_text="URL", blank=True)
    google = models.CharField(max_length=500, help_text="URL", blank=True)
    website = models.CharField(max_length=500, help_text="URL", blank=True)
    content = models.TextField(u'Content', blank=True)
    slug = models.SlugField(unique=True, blank=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_full_name(self):
        """ Return the email."""
        return self.email

    def get_short_name(self):
        """ Return the email."""
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """ Send an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = MakeSlug(self.name)
        super(AbstractAccount, self).save(*args, **kwargs)


class Account(AbstractAccount):

    """
    Concrete class of AbstractEmailUser.

    Use this if you don't need to extend EmailUser.

    """

    class Meta(AbstractAccount.Meta):
        swappable = 'AUTH_USER_MODEL'