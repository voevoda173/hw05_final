from django.contrib import admin

from .models import Comment, Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Класс PostAdmin используется для оформления и настройки
    интерфейса администратора сайта.
    """

    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'description',
    )
    search_fields = (
        'title',
        'description',
    )
    empty_value_display = '-пусто-'


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = (
        'pk',
        'post',
        'author',
        'created',
        'text',
    )
    search_fields = ('text',)
    list_filter = ('created', 'author',)
