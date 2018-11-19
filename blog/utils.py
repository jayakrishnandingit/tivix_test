import re

import bleach
from django.utils.text import slugify


def generate_slug(string, allow_unicode=True):
    """
    A util to generate a slug from a string.
    We enable unicode handling by default as opposed to django's slugify.
    """
    return slugify(string, allow_unicode=allow_unicode)


def allow_clean_links(tag, attr_name, attr_value):
    """
    Utility method to sanitize HTML <a> tags by removing
    any javascript or vbscripts in href attribute.
    """
    rjs = r'[\s]*(&#x.{1,7})?'.join(list('javascript:'))
    rvb = r'[\s]*(&#x.{1,7})?'.join(list('vbscript:'))
    re_scripts = re.compile('(%s)|(%s)' % (rjs, rvb), re.IGNORECASE)
    if attr_name == 'href':
        # if no javascript/vbscript found return True.
        return re.search(re_scripts, attr_value) is None
    if attr_name == 'title' or attr_name == 'target':
        return True
    return False


def clean_value(
        yucky_text,
        tags=bleach.sanitizer.ALLOWED_TAGS,
        attrs=bleach.sanitizer.ALLOWED_ATTRIBUTES,
        styles=bleach.sanitizer.ALLOWED_STYLES):
    """
    Utility method to clean fields from malicious HTML tags and attributes.
    """
    return bleach.clean(
        yucky_text,
        tags=tags,
        attributes=attrs,
        styles=styles,
        strip=True,
        strip_comments=True
    )
