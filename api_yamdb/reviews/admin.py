from django.contrib import admin

from reviews.models import Category, Genre, Title, GenreTitle, Review

admin.site.register(Review)

class GenreTitleInline(admin.TabularInline):
    model = GenreTitle
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройки отображения модели Category в админке."""

    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Настройки отображения модели Genre в админке."""

    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Настройки отображения модели Title в админке."""

    list_display = ('pk', 'name', 'year', 'category')
    search_fields = ('name',)
    list_filter = ('year', 'category')
    empty_value_display = '-пусто-'
    inlines = [GenreTitleInline]


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    """Настройки отображения модели GenreTitle в админке."""

    list_display = ('pk', 'title', 'genre')
    search_fields = ('title__name', 'genre__name')
    empty_value_display = '-пусто-'
