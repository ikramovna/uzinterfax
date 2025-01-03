from django.test import TestCase, Client
from django.urls import reverse
from main.models import NewsModel, ZoneModel, CategoryModel, TagModel
from django.core.files.uploadedfile import SimpleUploadedFile


class MainViewsTest(TestCase):
    def setUp(self):
        self.zone = ZoneModel.objects.create(name="Test Zone", slug="test-zone")
        self.category = CategoryModel.objects.create(name="Test Category", slug="test-category")

        temp_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'file_content',
            content_type='image/jpeg'
        )

        self.news = NewsModel.objects.create(
            title="Test News",
            short_description="Short description",
            content="Detailed content of the news",
            zone=self.zone,
            category=self.category,
            image=temp_image,
            is_chosen=True,
            is_breaking_new=True,
            is_article=True,
            is_photo_news=True,
        )

        self.tag = TagModel.objects.create(name="Test Tag", slug="test-tag")
        self.tag.news.add(self.news)

        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_chosen_view(self):
        response = self.client.get(reverse('chosen'))
        self.assertEqual(response.status_code, 200)

    def test_ads_view(self):
        response = self.client.get(reverse('ads'))
        self.assertEqual(response.status_code, 200)

    def test_articles_view(self):
        response = self.client.get(reverse('articles'))
        self.assertEqual(response.status_code, 200)

    def test_breaking_news_view(self):
        response = self.client.get(reverse('breaking_news'))
        self.assertEqual(response.status_code, 200)

    def test_category_view(self):
        response = self.client.get(reverse('category', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)

    def test_interviews_view(self):
        response = self.client.get(reverse('interviews'))
        self.assertEqual(response.status_code, 200)

    def test_inquiries_view(self):
        response = self.client.get(reverse('inquiries'))
        self.assertEqual(response.status_code, 200)

    def test_last_posts_view(self):
        response = self.client.get(reverse('last-posts', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_news_detail_view(self):
        response = self.client.get(reverse('news_detail', args=[self.news.slug]))
        self.assertEqual(response.status_code, 200)

    def test_region_view(self):
        response = self.client.get(reverse('region', args=[self.zone.slug]))
        self.assertEqual(response.status_code, 200)

    def test_tags_view(self):
        response = self.client.get(reverse('tags', args=[self.tag.slug, 1]))
        self.assertEqual(response.status_code, 200)

    def test_photonews_view(self):
        response = self.client.get(reverse('photonews'))
        self.assertEqual(response.status_code, 200)

