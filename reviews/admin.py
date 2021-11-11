from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"
    prepopulated_fields = {"slug": ("name",)}


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"
    prepopulated_fields = {"slug": ("name",)}


class TitleAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "year",
        "description",
        "category",
        "show_genres",
    ]
    search_fields = ("name",)
    list_filter = ("genre",)
    empty_value_display = "-пусто-"

    def show_genres(self, obj):
        return "\n".join([genre_item.name for genre_item in obj.genre.all()])


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "author",
        "title",
    )
    search_fields = ("text",)
    list_filter = ("title",)
    empty_value_display = "-пусто-"


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "author",
        "review",
    )
    search_fields = ("text",)
    list_filter = ("review",)
    empty_value_display = "-пусто-"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
