from django.db import models

from blog.utils import generate_slug


# Create your models here.
class TimestampMixin(models.Model):
    """
    A simple abstract model class to serve as a mixin for django models
    that require a timestamp during insertion.
    """
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class BlogPost(TimestampMixin):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, allow_unicode=True)
    description = models.TextField(max_length=1000)
    # keeping it simple. we just need to know who is the author.
    author = models.EmailField()

    def save(self, **kwargs):
        """
        Override django Model save method to
        generate a slug from the title during create.
        """
        created = self.pk is None
        if created and not self.slug:
            self.slug = generate_slug(self.title)
        super(BlogPost, self).save(**kwargs)

    def __str__(self):
        return self.title
