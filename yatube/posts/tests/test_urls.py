from http import HTTPStatus

from django.test import Client, TestCase

from ..models import Follow, Group, Post, User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_author = User.objects.create_user(username='TestAuthor')
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='test-slug',
            description='Тестовое описание',
        )

        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user_author,
            group=cls.group,
        )

    def setUp(self):
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.post_author = Client()
        self.post_author.force_login(self.user_author)

    def test_urls_exist_at_desired_location_none_auth(self):
        """Проверка страниц, доступных любому пользователю."""
        urls = {
            '/': HTTPStatus.OK,
            '/group/test-slug/': HTTPStatus.OK,
            f'/profile/{self.user_author.username}/': HTTPStatus.OK,
            f'/posts/{self.post.id}/': HTTPStatus.OK,
            f'/posts/{self.post.id}/comment/': HTTPStatus.FOUND,
        }
        for url, status_code in urls.items():
            with self.subTest(url=url):
                responce = self.client.get(url)
                self.assertEqual(responce.status_code, status_code)

    def test_urls_exist_at_desired_location_auth(self):
        """Проверка страниц, доступных только авторизованному пользователю."""
        urls = {
            '/create/': HTTPStatus.OK,
            f'/posts/{self.post.id}/comment/': HTTPStatus.FOUND,
        }
        for url, status_code in urls.items():
            with self.subTest(url=url):
                responce = self.authorized_client.get(url)
                self.assertEqual(responce.status_code, status_code)

    def test_urls_exist_at_desired_location_author(self):
        """Проверка страниц, доступных только автору."""
        urls = [
            f'/posts/{self.post.id}/edit/',
        ]
        for url in urls:
            with self.subTest(url=url):
                responce = self.post_author.get(url)
                self.assertEqual(responce.status_code, HTTPStatus.OK)

    def test_url_unexisting_page(self):
        """Проверка запроса к несуществующей странице"""
        response = self.client.get('/unexisting-page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_post_edit_url_redirect_no_author_on_post_detail(self):
        """Проверка редиректа не автора поста при попытке редактирования"""
        response = self.authorized_client.get(
            f'/posts/{self.post.id}/edit/', follow=True)
        self.assertRedirects(
            response, f'/posts/{self.post.id}/')

    def test_create_or_edit_url_redirect_anonymus_on_login(self):
        """Проверка редиректа анонимного пользователя
        при попытке создания, редактирования поста или
        комментирования поста."""
        urls = {
            '/create/': '/auth/login/?next=/create/',
            f'/posts/{self.post.id}/edit/':
            f'/auth/login/?next=/posts/{self.post.id}/edit/',
            f'/posts/{self.post.id}/comment/':
            f'/auth/login/?next=/posts/{self.post.id}/comment/',
        }
        for url, redirect in urls.items():
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertRedirects(response, redirect)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_urls_names = {
            '/': 'posts/index.html',
            '/group/test-slug/': 'posts/group_list.html',
            '/profile/TestAuthor/': 'posts/profile.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
            f'/posts/{self.post.id}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }
        for address, template in templates_urls_names.items():
            with self.subTest(address=address):
                response = self.post_author.get(address)
                self.assertTemplateUsed(response, template)

    def test_url_follow_exist_and_desired_auth(self):
        """Проверка, что авторизованный пользователь может
        подписываться на других пользователей."""
        self.authorized_client.get(
            f'/profile/{self.user_author.username}/follow/'
        )
        self.assertTrue(
            Follow.objects.filter(user=self.user,
                                  author=self.user_author)
        )

    def test_urk_unfollow_exist_and_desired_auth(self):
        """Проверка, что авторизованный пользователь может
        отписываться от других пользователей."""
        self.authorized_client.get(
            f'/profile/{self.user_author.username}/unfollow/'
        )
        self.assertFalse(
            Follow.objects.filter(user=self.user,
                                  author=self.user_author)
        )
