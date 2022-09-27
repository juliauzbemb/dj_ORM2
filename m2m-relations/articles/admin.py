from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import Article, Scope, Tag


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        tag_counter = 0
        for form in self.forms:
            form.cleaned_data
            if form.cleaned_data['is_main'] == 1:
                tag_counter += 1
        if tag_counter == 0:
            raise ValidationError('Укажите основной раздел')
        elif tag_counter > 1:
            raise ValidationError('Основным может быть только 1 раздел')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']