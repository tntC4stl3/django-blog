from django.conf.urls import url

from . import views
from .feeds import BlogFeed

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<year>\d+)/(?P<month>\d+)/(?P<slug>[\w|\-]+)$',
        views.ArticleDetailView.as_view(),
        name='detail'),
    url(r'^archives/$', views.Archives.as_view(),
        name='archives'),
    url(r'^categories/$', views.Categories.as_view(),
        name='categories'),
    url(r'^category/(?P<slug>\w+)/$', views.CategoryListView.as_view(),
        name='category'),
    url(r'^tags/$', views.Tags.as_view(), name='tags'),
    url(r'^tag/(?P<slug>[\w|\-]+)/$', views.TagsListView.as_view(),
        name='tag'),
    url(r'^feeds/atom/$', BlogFeed()),
]
