import shutil
import tempfile

from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..forms import PostForm
from ..models import Comment, Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='TestAuthor')
        cls.group = Group.objects.create(
            title='Тестовая группы',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.image = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='image.jpg',
            content=cls.image,
            content_type='image/jpg',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.author,
            group=cls.group,
            image=cls.uploaded,
        )

        cls.form = PostForm()

    def setUp(self):
        self.user = User.objects.create_user(username='TestUser')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author_client = Client()
        self.author_client.force_login(self.author)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_authorized_user_create_post(self):
        """Проверка создания записи авторизированным клиентом."""
        image = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )

        uploaded = SimpleUploadedFile(
            name='image_for_create.jpg',
            content=image,
            content_type='image/jpg',
        )
        post_count = Post.objects.count()
        form_data = {
            'text': 'Новый пост',
            'group': self.group.id,
            'image': uploaded,
        }
        self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        cache.clear()
        self.assertEqual(Post.objects.count(), post_count + 1)
        created_post = Post.objects.first()
        self.assertEqual(created_post.text, form_data['text'])
        self.assertEqual(created_post.group.slug, self.group.slug)
        self.assertEqual(created_post.author.id, self.user.id)
        self.assertEqual(created_post.image.name, f'posts/{uploaded.name}')

    def test_author_user_edit_post(self):
        """Проверка изменения поста при его редактировании автором."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Отредактированный пост',
            'author': self.author,
        }
        self.author_client.post(
            reverse('posts:post_edit', args=(self.post.id,)),
            data=form_data,
            follow=True,
        )
        self.assertEqual(
            Post.objects.get(pk=self.post.id).text, form_data['text']
        )
        self.assertEqual(Post.objects.count(), posts_count)

    def test_add_comment_auth(self):
        """Проверка добавления комментария авторизованным пользователем,
        а также его добавления на страницу поста."""
        comment_count = Comment.objects.count()
        comment = 'Тестовый комментарий'
        form_data = {
            'text': comment,
        }
        self.authorized_client.post(
            reverse('posts:add_comment', args=(self.post.id,)),
            data=form_data,
            follow=True,
        )
        self.assertEqual(Comment.objects.count(), comment_count + 1)
        comment_object = Comment.objects.latest('created')
        self.assertEqual(comment_object.text, comment)
        self.assertEqual(comment_object.post.id, self.post.id)
        self.assertEqual(comment_object.author.id, self.user.id)
