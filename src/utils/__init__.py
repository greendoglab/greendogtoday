"""
Methods fo processing content. Current version:
* Markdown compilation
* Create slug from title

requirements:
https://pypi.python.org/pypi/Markdown
https://github.com/dimka665/awesome-slugify
"""

import markdown
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from slugify import slugify
# import re
from sorl.thumbnail import default

MARKDOWN_EXTANTIOS = ['nl2br', 'tables', 'attr_list', 'extra']


# Make html from markdown
def MakeContent(value):
    return mark_safe(
        markdown.markdown(
            force_unicode(value),
            MARKDOWN_EXTANTIOS,
            safe_mode=False,
            enable_attributes=True
        )
    )


# Make SLug
def MakeSlug(value):
    if len(slugify(value, to_lower=True)) > 255:
        return slugify(value[:254], to_lower=True)
    else:
        return slugify(value, to_lower=True)


def MakeImage(image, thumbs, crop=None):
    if crop:
        thumb = default.backend.get_thumbnail(
            image,
            thumbs,
            crop=crop,
            quality=55
        )
    else:
        thumb = default.backend.get_thumbnail(
            image,
            thumbs,
            quality=55
        )
    return {'url': thumb.url}
