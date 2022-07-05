from django.contrib.auth import get_user_model
from django.db import models

from .constants import LEN_STR

User = get_user_model()


class Group(models.Model):
    """"
    Класс Group предназначен для создания групп,
    которые объединяют посты всех пользователей
    по определенной теме(направлению).
    Имеет следующие параметры:
    title - Наименование тематической группы,
    slug - значение, необходимое для формирования URL-адреса группы,
    description - описание (в том числе различные правила) тематической группы.
    """

    title = models.CharField(
        verbose_name='Название сообщества',
        max_length=200,
    )
    slug = models.SlugField(
        verbose_name='Адрес',
        unique=True,
    )
    description = models.TextField(
        verbose_name='Описание',
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(models.Model):
    """
    Класс Post предназначен для создания публикаций пользователей.
    Имеет следующие параметры:
    text - текст публикации,
    pub_date - дата публикации,
    author - автор публикации,
    group - тематическая группа, к которой относится публикация,
    LEN_STR - длина поста для вывода в консоль.
    """

    text = models.TextField(
        verbose_name='Текст',
        help_text='Выскажи свои мысли здесь',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        help_text='Когда высказана мысль',
        auto_now_add=True,
        db_index=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        help_text='Ну и кто же это придумал?',
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        Group,
        verbose_name='Сообщество',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='В каком сообществе опубликовать?',
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='posts/',
        blank=True,
        help_text='Здесь можно прикрепить картинку.',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        default_related_name = 'posts'

    def __str__(self):
        return self.text[:LEN_STR]


class Comment(models.Model):
    """Класс Comment предназначен для создания
    комментариев к опубликованным постам."""
    post = models.ForeignKey(
        Post,
        verbose_name='Комментарий',
        help_text='Хотите прокомментировать?',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Комментатор',
        help_text='Кто комментирует мысли?',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Что вы об этом думаете?',
    )
    created = models.DateTimeField(
        verbose_name='Дата комментария',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return self.text[:LEN_STR]


class Follow(models.Model):
    """Класс Follow предназначен для создания
    подписчиков на авторов."""
    user = models.ForeignKey(
        User,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Пользователь, который следит за постами автора.',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        verbose_name='Автор',
        help_text='Автор, у которого есть подписчики.',
        on_delete=models.CASCADE,
    )
