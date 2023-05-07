from django.test import SimpleTestCase
from django.urls import reverse, resolve
from blog.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, ImageDownloadView, about, search

class TestUrls(SimpleTestCase):

    def test_about_url_resolves(self):
        url = reverse('blog-about')
        self.assertEquals(resolve(url).func, about)

    def test_search_url_resolves(self):
        url = reverse('search')
        self.assertEquals(resolve(url).func, search)

    def test_home_url_resolves(self):
        url = reverse('blog-home')
        self.assertEquals(resolve(url).func.view_class, PostListView)

    def test_post_new_url_resolves(self):
        url = reverse('blog-new')
        self.assertEquals(resolve(url).func.view_class, PostCreateView)

    def test_post_detail_url_resolves(self):
        url = reverse('blog-detail', args=[1])  # assuming post id is 1
        self.assertEquals(resolve(url).func.view_class, PostDetailView)

    def test_post_update_url_resolves(self):
        url = reverse('blog-update', args=[1])  # assuming post id is 1
        self.assertEquals(resolve(url).func.view_class, PostUpdateView)

    def test_post_delete_url_resolves(self):
        url = reverse('blog-delete', args=[1])  # assuming post id is 1
        self.assertEquals(resolve(url).func.view_class, PostDeleteView)

    def test_image_download_url_resolves(self):
        url = reverse('image_download', args=[1])  # assuming image id is 1
        self.assertEquals(resolve(url).func.view_class, ImageDownloadView)
