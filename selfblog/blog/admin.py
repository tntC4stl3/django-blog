from django.contrib import admin

# Register your models here.
from .models import Category, Article, Page, Tag
from .forms import ArticleForm


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Page)
