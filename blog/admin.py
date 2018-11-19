from django.contrib import admin

from blog.models import BlogPost


# Register your models here.
class BlogPostAdmin(admin.ModelAdmin):
    pass


admin.site.register(BlogPost, BlogPostAdmin)
