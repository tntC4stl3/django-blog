# coding: utf-8


import markdown2

from django.db import models


STATUS = {
    0: 'Publish',
    1: 'Draft',
    2: 'Hidden',
}


class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name='Name', unique=True)
    slug = models.SlugField(max_length=40, verbose_name='Slug')

    created_time = models.DateTimeField('Created Date', auto_now_add=True,
                                        editable=True)
    updated_time = models.DateTimeField('Updated Date', auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = verbose_name = "Categories"


class Tag(models.Model):
    name = models.CharField(max_length=40, verbose_name='Name', unique=True)
    slug = models.SlugField(max_length=40, verbose_name='Slug')

    created_time = models.DateTimeField('Created Date', auto_now_add=True)
    updated_time = models.DateTimeField('Updated Date', auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = verbose_name = "Tags"


class Article(models.Model):
    category = models.ForeignKey(Category, verbose_name='Category')

    title = models.CharField(max_length=100, verbose_name='Title')
    slug = models.SlugField(max_length=100, verbose_name='Slug')
    content = models.TextField(verbose_name='Content')
    content_html = models.TextField(verbose_name='Html Content', editable=False)
    tags = models.ManyToManyField(Tag, verbose_name='Tags',
                                  related_name='articles', blank=True,
                                  help_text='Split with comma')
    status = models.IntegerField(default=1, choices=list(STATUS.items()),
                                 verbose_name='Status')

    published_time = models.DateTimeField('Published Date', auto_now_add=True,
                                          editable=True)
    updated_time = models.DateTimeField('Updated Date', auto_now=True)

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
            extras=['fenced-code-blocks'])
        super(Article, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-published_time']
        verbose_name_plural = verbose_name = 'Articles'


class Page(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    slug = models.SlugField(max_length=100, verbose_name='Slug')
    content = models.TextField(verbose_name='Content')
    content_html = models.TextField(verbose_name='HTML Content',
                                    editable=False)

    rank = models.IntegerField(default=1, verbose_name='Rank',
                               help_text='Display order')
    status = models.IntegerField(default=1, choices=list(STATUS.items()),
                                 verbose_name='Status')

    created_time = models.DateTimeField('Created Date', auto_now_add=True)
    updated_time = models.DateTimeField('Updated Date', auto_now=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.content_html = markdown2.markdown(
            self.content,
            extras=['fenced-code-blocks'])
        super(Page, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-rank', '-created_time']
        verbose_name_plural = verbose_name = "Pages"
