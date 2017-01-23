from datetime import datetime
from time import sleep
from django.test import TestCase
from django.db.models import Q
from .models import Category, Article, Page, Tag


class ArticleModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Python', slug='python')

    def test_convert_article_content_to_html(self):
        article = Article.objects.create(category=self.category,
                                         title='Django test',
                                         slug='django-test',
                                         content='# Django Test')
        self.assertHTMLEqual(article.content_html, '<h1>Django Test</h1>\n')

    def test_article_has_correct_custom_property(self):
        article = Article.objects.create(category=self.category,
                                         title='Django test1',
                                         slug='django-test1',
                                         content='# Django Test')
        today = datetime.utcnow()
        self.assertEqual(article.year, today.year)
        self.assertEqual(article.month, today.month)


class PageModelTest(TestCase):
    def test_convert_page_content_to_html(self):
        page = Page.objects.create(title='About',
                                   slug='about',
                                   content='# About')
        self.assertHTMLEqual(page.content_html, '<h1>About</h1>\n')


class IndexViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Python', slug='python')

    def test_uses_index_template(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'blog/index.html')

    def test_index_is_first_page(self):
        response = self.client.get('/')

        self.assertEqual(response.context['articles_list'].number, 1)

    def test_show_first_page_if_request_page_is_not_integer(self):
        response = self.client.get('/?page=NotInteger')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['articles_list'].number, 1)

    def test_show_first_page_if_request_page_is_negative(self):
        response = self.client.get('/?page=-1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['articles_list'].number, 1)

    def test_show_first_page_if_request_page_is_out_of_range(self):
        response = self.client.get('/?page=999999')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['articles_list'].number, 1)

    def test_page_has_correct_articles(self):
        Article.objects.create(category=self.category,
                               title='Django test',
                               slug='django-test',
                               content='# Django Test',
                               status=0)
        Article.objects.create(category=self.category,
                               title='Django test1',
                               slug='django-test-1',
                               content='# Django Test 1',
                               status=1)
        Article.objects.create(category=self.category,
                               title='Django test2',
                               slug='django-test-2',
                               content='# Django Test 2',
                               status=2)

        response = self.client.get('/')

        # only articles with status publish will show on the page
        articles_list = response.context['articles_list']
        self.assertEqual(len(articles_list), 1)
        article = articles_list[0]
        self.assertEqual(article.title, 'Django test')


class ArticleDetailViewTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Python', slug='python')
        Article.objects.create(category=category,
                               title='Django test',
                               slug='django-test',
                               content='# Django Test',
                               status=0)
        Article.objects.create(category=category,
                               title='Django test1',
                               slug='django-test-1',
                               content='# Django Test 1',
                               status=1)
        Article.objects.create(category=category,
                               title='Django test2',
                               slug='django-test-2',
                               content='# Django Test 2',
                               status=2)

    def test_can_request_publish_article_via_slug(self):
        article = Article.objects.get(slug='django-test')
        response = self.client.get('/post/%d/%d/%s' % (article.year,
                                                       article.month,
                                                       article.slug))
        self.assertEqual(response.context['article'], article)

    def test_can_not_request_non_pub_article_via_slug(self):
        articles = Article.objects.filter(~Q(status=0))
        for article in articles:
            response = self.client.get('/post/%d/%d/%s' % (article.year,
                                                           article.month,
                                                           article.slug))
            self.assertEqual(response.status_code, 404)


class ArchivesViewTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Python', slug='python')
        Article.objects.create(category=category,
                               title='Django test',
                               slug='django-test',
                               content='# Django Test',
                               status=0)
        sleep(3)
        Article.objects.create(category=category,
                               title='Django test1',
                               slug='django-test-1',
                               content='# Django Test 1',
                               status=0)

    def test_can_get_right_archive_page(self):
        response = self.client.get('/archives/')
        articles = response.context['articles_list']

        self.assertEqual(len(articles), 2)
        self.assertEqual(articles[0].title, 'Django test1')
        self.assertEqual(articles[1].title, 'Django test')


class CategoriesTest(TestCase):
    def setUp(self):
        category_one = Category.objects.create(name='Python', slug='python')
        category_two = Category.objects.create(name='Linux', slug='linux')
        Article.objects.create(category=category_one,
                               title='Django test',
                               slug='django-test',
                               content='# Django Test',
                               status=0)
        Article.objects.create(category=category_one,
                               title='Django test1',
                               slug='django-test-1',
                               content='# Django Test 1',
                               status=1)
        Article.objects.create(category=category_two,
                               title='Django test2',
                               slug='django-test-2',
                               content='# Django Test 2',
                               status=2)

    def test_get_correct_categories_and_article_count(self):
        response = self.client.get('/categories/')
        categories = response.context['categories']

        # A category without any published articles should not be showed.
        self.assertEqual(len(categories), 1)
        # Non published article should not be calculated into total count
        self.assertEqual(categories[0][1], 1)

    def test_get_right_category_articles_list(self):
        response = self.client.get('/category/python/')
        articles_list = response.context['articles_list']

        # Get only one published article.
        self.assertEqual(len(articles_list), 1)
        self.assertEqual(articles_list[0].title, 'Django test')


class TagsTest(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Python', slug='python')
        tag_one = Tag.objects.create(name='Python', slug='python')
        tag_two = Tag.objects.create(name='Django', slug='django')
        tag_three = Tag.objects.create(name='Test', slug='test')
        article_one = Article.objects.create(category=category,
                                             title='Django test',
                                             slug='django-test',
                                             content='# Django Test',
                                             status=0)
        article_one.tags.add(tag_one, tag_two)
        article_two = Article.objects.create(category=category,
                                             title='Django test1',
                                             slug='django-test-1',
                                             content='# Django Test 1',
                                             status=1)
        article_two.tags.add(tag_one)
        article_three = Article.objects.create(category=category,
                                               title='Django test2',
                                               slug='django-test-2',
                                               content='# Django Test 2',
                                               status=0)
        article_three.tags.add(tag_two)
        article_four = Article.objects.create(category=category,
                                              title='Django test3',
                                              slug='django-test-3',
                                              content='# Django Test 3',
                                              status=2)
        article_four.tags.add(tag_three)

    def test_get_correct_tags_and_article_counts(self):
        response = self.client.get('/tags/')
        tags = response.context['tags']

        self.assertEqual(len(tags), 2)
        # The tags is in dictionary order.
        self.assertEqual(tags[0][0].name, 'Django')
        self.assertEqual(tags[0][1], 2)
        self.assertEqual(tags[1][0].name, 'Python')
        self.assertEqual(tags[1][1], 1)

    def test_get_right_tag_articles_list(self):
        response = self.client.get('/tag/python/')
        articles_list = response.context['articles_list']

        # Get only one published article.
        self.assertEqual(len(articles_list), 1)
        self.assertEqual(articles_list[0].title, 'Django test')
