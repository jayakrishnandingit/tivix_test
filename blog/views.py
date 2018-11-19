from django.shortcuts import render
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from blog.models import BlogPost
from blog.forms import BlogPostForm


# Create your views here.
class BlogPostList(ListView):
    """
    View to list all blogs.
    """
    model = BlogPost
    template_name = 'blog/blog_post_list.html'
    context_object_name = 'blogs'


class BlogPostCreate(CreateView):
    """
    View to create a new blog post.
    Once created it redirects to blog details page.
    """
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blog_post_create.html'

    def form_valid(self, form):
        """
        Override form_valid method to assign slug generated from title
        into slug field in the instance so that it can be persisted to DB.

        slug field was excluded from form fields since we do not allow
        it to be edited by user.
        """
        # we have generated slug in the form during validation.
        form.instance.slug = form.slug
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Method used to render erroneous form back to the user.

        Also flash a message saying an error occurred.
        """
        messages.error(self.request, _("Please correct the errors and submit again."))
        return super().form_invalid(form)

    def get_success_url(self):
        """
        Method to return the URL to redirect to after successful save.

        Perfect place to flash a success message.
        """
        messages.success(self.request, _("Blog post created!"))
        return super().get_success_url()



class BlogPostDetail(DetailView):
    """
    View to display the details about a blog post.

    We use slug to query the blog.
    """
    model = BlogPost
    template_name = 'blog/blog_post_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'blog'


class BlogPostUpdate(UpdateView):
    """
    View to update a blog post.

    We use the primary key to query the blog post in this case.
    """
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blog_post_update.html'

    def form_invalid(self, form):
        """
        Method used to render erroneous form back to the user.

        Also flash a message saying an error occurred.
        """
        messages.error(self.request, _("Please correct the errors and submit again."))
        return super().form_invalid(form)

    def get_success_url(self):
        """
        Method to return the URL to redirect to after successful save.

        Perfect place to flash a success message.
        """
        messages.success(self.request, _("Blog post saved!"))
        return super().get_success_url()

