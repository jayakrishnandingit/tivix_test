from django.shortcuts import render
from django.views.generic import ListView

from blog.models import BlogPost


# Create your views here.
class BlogPostList(ListView):
    model = BlogPost
    template_name = 'blog/blog_post_list.html'
    context_object_name = 'blogs'




