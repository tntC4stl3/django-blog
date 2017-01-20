# coding: utf-8
import logging

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404

from .models import Category, Article, Tag, Page
from .constants import ITEMS_PER_PAGE


logger = logging.getLogger(__name__)


class IndexView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'articles_list'

    def get(self, request, *args, **kwargs):
        # If page is not an integer or less than 1, deliver first page.
        try:
            self.current_page = int(request.GET.get('page', 1))
        except ValueError:
            self.current_page = 1

        if self.current_page < 1:
            self.current_page = 1

        return super(IndexView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        articles_list = Article.objects.filter(status=0)
        return articles_list

    def get_context_data(self, **kwargs):
        paginator = Paginator(self.object_list, ITEMS_PER_PAGE)
        try:
            items = paginator.page(self.current_page)
        except EmptyPage:
            items = paginator.page(1)
        kwargs[self.context_object_name] = items
        return super(IndexView, self).get_context_data(**kwargs)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'

    def get_object(self):
        article = super(ArticleDetailView, self).get_object()
        if article is not None and article.status != 0:
            raise Http404
        return article


class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/page.html'
    context_object_name = 'page'

    def get_object(self):
        page = super(PageDetailView, self).get_object()
        if page is not None and page.status != 0:
            raise Http404
        return page


class Archives(ListView):
    template_name = 'blog/archives.html'
    context_object_name = 'articles_list'

    def get_queryset(self):
        articles_list = Article.objects.filter(status=0).only(
            'id', 'title', 'published_time').order_by('-published_time')
        return articles_list


class Categories(ListView):
    template_name = 'blog/categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        categories = Category.objects.filter(article__status=0)
        category_article_count = {}
        for category in categories:
            category_article_count[category] = \
                category_article_count.get(category, 0) + 1
        return sorted(category_article_count.items(), key=lambda k: k[0].name)


class CategoryListView(IndexView):
    template_name = 'blog/index.html'
    context_object_name = 'articles_list'

    def get_queryset(self):
        articles_list = Article.objects.filter(
            category__slug=self.kwargs['slug'],
            status=0)
        return articles_list


class Tags(ListView):
    template_name = 'blog/tags.html'
    context_object_name = 'tags'

    def get_queryset(self):
        tags = Tag.objects.filter(articles__status=0)
        tag_article_count = {}
        for tag in tags:
            tag_article_count[tag] = \
                tag_article_count.get(tag, 0) + 1
        return sorted(tag_article_count.items(), key=lambda k: k[0].name)


class TagsListView(IndexView):
    context_object_name = 'articles_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        articles_list = Article.objects.filter(
            status=0,
            tags__in=[tag])
        return articles_list
