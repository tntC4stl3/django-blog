# coding: utf-8
from __future__ import unicode_literals

import markdown2

from django.db import models


STATUS = {
    0: u'Publish',
    1: u'Draft',
    2: u'Hidden',
}


class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name=u'Name', unique=True)
    slug = models.SlugField(max_length=40, verbose_name=u'Slug')

    created_time = models.DateTimeField(u'Created Date', auto_now_add=True,
                                        editable=True)
    updated_time = models.DateTimeField(u'Updated Date', auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = verbose_name = u"Categories"


class Tag(models.Model):
    name = models.CharField(max_length=40, verbose_name=u'Name', unique=True)
    slug = models.SlugField(max_length=40, verbose_name=u'Slug')

    created_time = models.DateTimeField(u'Created Date', auto_now_add=True)
    updated_time = models.DateTimeField(u'Updated Date', auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = verbose_name = u"Tags"


class Article(models.Model):
    category = models.ForeignKey(Category, verbose_name=u'Category')

    title = models.CharField(max_length=100, verbose_name=u'Title')
    slug = models.SlugField(max_length=100, verbose_name=u'Slug')
    content = models.TextField(verbose_name=u'Content')
    content_html = models.TextField(verbose_name=u'Html Content', editable=False)
    tags = models.ManyToManyField(Tag, verbose_name=u'Tags',
                                  related_name='articles', blank=True,
                                  help_text=u'Split with comma')
    status = models.IntegerField(default=1, choices=STATUS.items(),
                                 verbose_name=u'Status')

    published_time = models.DateTimeField(u'Published Date', auto_now_add=True,
                                          editable=True)
    updated_time = models.DateTimeField(u'Updated Date', auto_now=True)

    def __unicode__(self):
        return self.title

    @property
    def year(self):
        return self.published_time.year

    @property
    def month(self):
        return self.published_time.month

    def save(self, *args, **kwargs):
        self.content_html = markdown2.markdown(
            self.content,
            extras=['fenced-code-blocks']).encode('utf-8')
        super(Article, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-published_time']
        verbose_name_plural = verbose_name = u'Articles'


class Page(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'Title')
    slug = models.SlugField(max_length=100, verbose_name=u'Slug')
    content = models.TextField(verbose_name=u'Content')
    content_html = models.TextField(verbose_name=u'HTML Content',
                                    editable=False)

    rank = models.IntegerField(default=1, verbose_name=u'Rank',
                               help_text=u'Display order')
    status = models.IntegerField(default=1, choices=STATUS.items(),
                                 verbose_name=u'Status')

    created_time = models.DateTimeField(u'Created Date', auto_now_add=True)
    updated_time = models.DateTimeField(u'Updated Date', auto_now=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.content_html = markdown2.markdown(
            self.content,
            extras=['fenced-code-blocks']).encode('utf-8')
        super(Page, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-rank', '-created_time']
        verbose_name_plural = verbose_name = u"Pages"
