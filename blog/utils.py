from django.utils.text import slugify


def generate_slug(string, allow_unicode=True):
    """
    A util to generate a slug from a string.
    We enable unicode handling by default as opposed to django's slugify.
    """
    return slugify(string, allow_unicode=allow_unicode)
