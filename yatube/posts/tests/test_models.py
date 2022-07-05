from django.test import TestCase

from ..constants import LEN_STR
from ..models import Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост' * 5,
        )

    def test_model_post_have_correct_object_names(self):
        """Проверяем, что в моделях корректно работает __str__."""
        post = PostModelTest.post
        group = PostModelTest.group
        text = post.text[:LEN_STR]
        title = group.title
        model_fields = {
            text: post,
            title: group,
        }
        for field, expected_value in model_fields.items():
            with self.subTest(field=field):
                self.assertEqual(field, str(expected_value))

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        verbose_fields = {
            'text': 'Текст',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Сообщество',
            'image': 'Изображение',
        }
        for field, expected_value in verbose_fields.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        help_text_fields = {
            'text': 'Выскажи свои мысли здесь',
            'pub_date': 'Когда высказана мысль',
            'author': 'Ну и кто же это придумал?',
            'group': 'В каком сообществе опубликовать?',
            'image': 'Здесь можно прикрепить картинку.',
        }
        for field, expected_value in help_text_fields.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value)
