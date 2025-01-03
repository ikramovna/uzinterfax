from django.test import TestCase
from main.models import ZoneModel, CategoryModel, NewsModel, TagModel


class ZoneModelTest(TestCase):
    def setUp(self):
        self.zone = ZoneModel.objects.create(name="Test Zone")

    def test_zone_creation(self):
        self.assertEqual(self.zone.name, "Test Zone")
        self.assertTrue(isinstance(self.zone, ZoneModel))
        self.assertEqual(str(self.zone), "Test Zone")

    def test_slug_generation(self):
        self.zone.save()
        self.assertEqual(self.zone.slug, "test-zone")

    def test_slug_uniqueness(self):
        ZoneModel.objects.create(name="Test Zone")
        second_zone = ZoneModel.objects.create(name="Test Zone")
        self.assertNotEqual(self.zone.slug, second_zone.slug)
        self.assertTrue(second_zone.slug.startswith("test-zone-"))


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = CategoryModel.objects.create(name="Test Category")

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Test Category")
        self.assertTrue(isinstance(self.category, CategoryModel))
        self.assertEqual(str(self.category), "Test Category")

    def test_slug_generation(self):
        self.category.save()
        self.assertEqual(self.category.slug, "test-category")

    def test_slug_uniqueness(self):
        CategoryModel.objects.create(name="Test Category")
        second_category = CategoryModel.objects.create(name="Test Category")
        self.assertNotEqual(self.category.slug, second_category.slug)
        self.assertTrue(second_category.slug.startswith("test-category-"))


class NewsModelTest(TestCase):
    def setUp(self):
        self.zone = ZoneModel.objects.create(name="Test Zone")
        self.category = CategoryModel.objects.create(name="Test Category")

        self.news = NewsModel.objects.create(
            title="Test News",
            short_description="A short description of the news.",
            content="This is the content of the test news.",
            zone=self.zone,
            category=self.category,
            is_chosen=True
        )

    def test_news_creation(self):
        self.assertEqual(self.news.title, "Test News")
        self.assertTrue(isinstance(self.news, NewsModel))
        self.assertEqual(str(self.news), "Test News")

    def test_slug_generation(self):
        self.news.save()
        self.assertEqual(self.news.slug, "test-news")

    def test_slug_uniqueness(self):
        NewsModel.objects.create(title="Test News")
        second_news = NewsModel.objects.create(title="Test News")
        self.assertNotEqual(self.news.slug, second_news.slug)
        self.assertTrue(second_news.slug.startswith("test-news-"))

    def test_related_zone_and_category(self):
        self.assertEqual(self.news.zone.name, "Test Zone")
        self.assertEqual(self.news.category.name, "Test Category")

    def test_optional_fields(self):
        news_without_optional = NewsModel.objects.create(
            title="News Without Optional Fields",
            content="Content only."
        )
        self.assertIsNone(news_without_optional.short_description)
        self.assertFalse(news_without_optional.image)
        self.assertIsNone(news_without_optional.zone)
        self.assertIsNone(news_without_optional.category)


class TagModelTest(TestCase):
    def setUp(self):
        self.news = NewsModel.objects.create(
            title="Sample News",
            content="Content for sample news."
        )

        self.tag = TagModel.objects.create(name="Test Tag")
        self.tag.news.add(self.news)

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, "Test Tag")
        self.assertTrue(isinstance(self.tag, TagModel))
        self.assertEqual(str(self.tag), "Test Tag")

    def test_slug_generation(self):
        self.tag.save()
        self.assertEqual(self.tag.slug, "test-tag")

    def test_slug_uniqueness(self):
        TagModel.objects.create(name="Test Tag")
        second_tag = TagModel.objects.create(name="Test Tag")
        self.assertNotEqual(self.tag.slug, second_tag.slug)
        self.assertTrue(second_tag.slug.startswith("test-tag-"))

    def test_many_to_many_relationship(self):
        self.assertIn(self.news, self.tag.news.all())
        self.assertEqual(self.news.tags.first(), self.tag)
