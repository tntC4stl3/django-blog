# coding: utf-8

from django import forms

from .models import Tag, Article


# support many to many tags column, input comma seperated tags in Admin
# page.
# https://groups.google.com/forum/#!topic/python-cn/f70UkfP6qCg
class TagWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        if value:
            value = ', '.join([o.name for o in value])
        else:
            value = ''
        return super(TagWidget, self).render(name, value, attrs)


class TagsField(forms.CharField):
    widget = TagWidget

    def clean(self, value):
        tagwords = [o.strip() for o in value.split(',') if o.strip()]
        return [Tag.objects.get_or_create(name=t.lower(), slug=t.lower())[0]
                for t in set(tagwords)]


class ArticleForm(forms.ModelForm):
    tags = TagsField(label=u"Tags", 
                     help_text=u"Please use comma to separate multiple tags.")

    class Meta:
        model = Article
        fields = '__all__'
