from django.test import TestCase
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from blog.models import BlogPost


# Create your tests here.
class BlogPostCreateTestCase(TestCase):
    def test_empty_values_fails(self):
        data = {
            'title': '',
            'description': 'Description',
            'author': 'jay@example.com'
        }
        response = self.client.post(reverse('blog-post-create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_post_create.html')
        self.assertFormError(response, 'form', 'title', [_("This field is required.")])

        data = {
            'description': 'Description',
            'author': 'jay@example.com'
        }
        response = self.client.post(reverse('blog-post-create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_post_create.html')
        self.assertFormError(response, 'form', 'title', [_("This field is required.")])

        data = {
            'title': 'I am a title!',
            'description': 'Description',
            'author': ''
        }
        response = self.client.post(reverse('blog-post-create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_post_create.html')
        self.assertFormError(response, 'form', 'author', [_("This field is required.")])

        data = {
            'title': 'I am a title!',
            'description': 'Description',
        }
        response = self.client.post(reverse('blog-post-create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_post_create.html')
        self.assertFormError(response, 'form', 'author', [_("This field is required.")])

    def test_invalid_title_fails(self):
        data = {
            'title': 123,
            'description': 'Description',
            'author': 'jay@example.com'
        }
        response = self.client.post(reverse('blog-post-create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_post_create.html')
        self.assertFormError(response, 'form', 'title', [_('Invalid value.')])

        data = {
            'title': '<a></a>',
            'description': 'Description',
            'author': 'jay@example.com'
        }
        response = self.client.post(reverse('blog-post-create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', [_('This field cannot be blank.')])

    def test_duplicate_title_fails(self):
        data = {
            'title': 'I am a title!',
            'description': 'Description',
            'author': 'jay@example.com'
        }
        response = self.client.post(reverse('blog-post-create'), data)
        self.assertEqual(response.status_code, 302)
        # repeat the same values.
        response = self.client.post(reverse('blog-post-create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', [_('Blog with a similar title already exists.')])

    def test_duplicate_non_ascii_title_fails(self):
        data = {
            'title': '初見米込能賀重再芸験田就例無面常',
            'description': '初見米込能賀重再芸験田就例無面常。未済毎掲屋日通治必数除申療合表',
            'author': 'xi@example.com'
        }
        response = self.client.post(reverse('blog-post-create'), data)
        self.assertEqual(response.status_code, 302)
        # repeat the same values.
        response = self.client.post(reverse('blog-post-create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', [_('Blog with a similar title already exists.')])

    def test_title_max_length_exceed_fails(self):
        data = {
            'title': (
                'Lorem ipsum ist ein pseudo-Lateinischer Text für Webdesign, '
                'Typografie, Layout und Printmedien. Er ersetzt Deutsch um '
                'Designelemente gegenüber dem Inhalt hervorzuheben, '
                'hat also die Funktion als Platzhalters in Layouts'
            ),
            'description': (
                'Lorem ipsum ist ein pseudo-Lateinischer Text für Webdesign, '
                'Typografie, Layout und Printmedien. Er ersetzt Deutsch um '
                'Designelemente gegenüber dem Inhalt hervorzuheben, '
                'hat also die Funktion als Platzhalters in Layouts'
            ),
            'author': 'jay@example.com'
        }
        response = self.client.post(reverse('blog-post-create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', _("Ensure this value has at most 100 characters (it has 218)."))

    def test_slug_never_exceeds_max_length(self):
        data = {
            'title': (
                'Worte gibt es gar nicht, das gilt auch für "Lorem". '
                'Einige Fragmente erinnern jedoch'
            ),
            'description': (
                'Lorem ipsum ist ein pseudo-Lateinischer Text für Webdesign, '
                'Typografie, Layout und Printmedien. Er ersetzt Deutsch um '
                'Designelemente gegenüber dem Inhalt hervorzuheben, '
                'hat also die Funktion als Platzhalters in Layouts'
            ),
            'author': 'jay@example.com'
        }
        response = self.client.post(reverse('blog-post-create'), data)
        self.assertEqual(response.status_code, 302)
        blog = BlogPost.objects.filter(title=data['title']).first()
        self.assertLessEqual(len(blog.slug), 50)
        self.assertRedirects(response, reverse('blog-post-detail', args=(blog.slug,)))

    def test_non_ascii_is_success(self):
        data = {
            'title': 'Text für Webdesign',
            'description': (
                'Lorem ipsum ist ein pseudo-Lateinischer Text für Webdesign, '
                'Typografie, Layout und Printmedien. Er ersetzt Deutsch um '
                'Designelemente gegenüber dem Inhalt hervorzuheben, '
                'hat also die Funktion als Platzhalters in Layouts'
            ),
            'author': 'jay@example.com'
        }
        response = self.client.post(reverse('blog-post-create'), data)
        self.assertEqual(response.status_code, 302)

        data = {
            'title': '初見米込能賀重再芸験田就例無面常',
            'description': '初見米込能賀重再芸験田就例無面常。未済毎掲屋日通治必数除申療合表',
            'author': 'xi@example.com'
        }
        response = self.client.post(reverse('blog-post-create'), data)
        self.assertEqual(response.status_code, 302)
        blog = BlogPost.objects.filter(author='xi@example.com').first()
        self.assertRedirects(response, reverse('blog-post-detail', args=(blog.slug,)))


class BlogPostListTestCase(TestCase):
    def test_list_view_shows_all_blogs(self):
        for i in range(100):
            data = {
                'title': 'I am a title %s!' % i,
                'description': 'Description',
                'author': 'jay@example.com'
            }
            self.client.post(reverse('blog-post-create'), data)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.context['blogs'].count(), 100)


class BlogPostUpdateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.blog1 = BlogPost(
            title='I am a title 1!',
            description='Description 1.',
            author='jay1@example.com'
        )
        cls.blog1.save()

        cls.blog2 = BlogPost(
            title='I am a title 2!',
            description='Description 2.',
            author='jay2@example.com'
        )
        cls.blog2.save()

    def test_empty_values_fails(self):
        data = {
            'title': '',
            'description': 'Description',
            'author': 'jay@example.com'
        }
        response = self.client.post(reverse('blog-post-update', args=(self.blog1.pk,)), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_post_update.html')
        self.assertFormError(response, 'form', 'title', [_("This field is required.")])

        data = {
            'description': 'Description',
            'author': 'jay@example.com'
        }
        response = self.client.post(reverse('blog-post-update', args=(self.blog1.pk,)), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_post_update.html')
        self.assertFormError(response, 'form', 'title', [_("This field is required.")])

        data = {
            'title': 'I am a title!',
            'description': 'Description',
            'author': ''
        }
        response = self.client.post(reverse('blog-post-update', args=(self.blog1.pk,)), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_post_update.html')
        self.assertFormError(response, 'form', 'author', [_("This field is required.")])

        data = {
            'title': 'I am a title!',
            'description': 'Description',
        }
        response = self.client.post(reverse('blog-post-update', args=(self.blog1.pk,)), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_post_update.html')
        self.assertFormError(response, 'form', 'author', [_("This field is required.")])

    def test_invalid_title_fails(self):
        data = {
            'title': 123,
            'description': 'Description',
            'author': 'jay1@example.com'
        }
        response = self.client.post(reverse('blog-post-update', args=(self.blog1.pk,)), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_post_update.html')
        self.assertFormError(response, 'form', 'title', [_('Invalid value.')])

        data = {
            'title': '<a></a>',
            'description': 'Description',
            'author': 'jay@example.com'
        }
        response = self.client.post(reverse('blog-post-update', args=(self.blog1.pk,)), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', [_('This field cannot be blank.')])

    def test_duplicate_title_fails(self):
        """
        Try to update blog1 with title of blog2.
        """
        data = {
            'title': 'I am a title 2!',
            'description': 'Description 1',
            'author': 'jay1@example.com'
        }
        response = self.client.post(reverse('blog-post-update', args=(self.blog1.pk,)), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', [_('Blog with a similar title already exists.')])

    def test_title_max_length_exceed_fails(self):
        data = {
            'title': (
                'Lorem ipsum ist ein pseudo-Lateinischer Text für Webdesign, '
                'Typografie, Layout und Printmedien. Er ersetzt Deutsch um '
                'Designelemente gegenüber dem Inhalt hervorzuheben, '
                'hat also die Funktion als Platzhalters in Layouts'
            ),
            'description': 'Description 1',
            'author': 'jay1@example.com'
        }
        response = self.client.post(reverse('blog-post-update', args=(self.blog1.pk,)), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', _("Ensure this value has at most 100 characters (it has 218)."))

    def test_slug_never_exceeds_max_length(self):
        data = {
            'title': (
                'Worte gibt es gar nicht, das gilt auch für "Lorem". '
                'Einige Fragmente erinnern jedoch'
            ),
            'description': (
                'Lorem ipsum ist ein pseudo-Lateinischer Text für Webdesign, '
                'Typografie, Layout und Printmedien. Er ersetzt Deutsch um '
                'Designelemente gegenüber dem Inhalt hervorzuheben, '
                'hat also die Funktion als Platzhalters in Layouts'
            ),
            'author': 'jay1@example.com'
        }
        response = self.client.post(reverse('blog-post-update', args=(self.blog1.pk,)), data)
        self.assertEqual(response.status_code, 302)
        blog = BlogPost.objects.filter(title=data['title']).first()
        self.assertLessEqual(len(blog.slug), 50)
        self.assertRedirects(response, reverse('blog-post-detail', args=(blog.slug,)))
