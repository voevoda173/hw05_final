from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class UserURLTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_exist_at_desired_location_none_auth(self):
        """Проверка страниц, доступных любому пользователю."""
        urls = [
            '/auth/signup/',
            '/auth/logout/',
            '/auth/login/',
            '/auth/password_reset/',
            '/auth/password_reset/done/',
            '/auth/reset/done/',
            '/auth/reset/<uidb64>/<token>/',
        ]
        for url in urls:
            with self.subTest(url=url):
                responce = self.client.get(url)
                self.assertEqual(responce.status_code, HTTPStatus.OK)

    def test_urls_exist_at_desired_location_auth(self):
        """Проверка страниц, доступных только авторизованному пользователю."""
        urls = [
            '/auth/password_change/',
            '/auth/password_change/done/',
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_unexisting_page(self):
        """Проверка запроса к несуществующей странице"""
        response = self.client.get('/auth/unexisting-page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_password_change_url_redirect_anonymus_on_login(self):
        """Проверка редиректа анонимного пользователя
        при попытке изменения пароля."""
        urls = {
            '/auth/password_change/':
            '/auth/login/?next=/auth/password_change/',
            '/auth/password_change/done/':
            '/auth/login/?next=/auth/password_change/done/',
        }
        for url, redirect in urls.items():
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertRedirects(response, redirect)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_urls_names = {
            '/auth/signup/': 'users/signup.html',
            '/auth/login/': 'users/login.html',
            '/auth/password_reset/': 'users/password_reset_form.html',
            '/auth/password_reset/done/': 'users/password_reset_done.html',
            '/auth/reset/done/': 'users/password_reset_complete.html',
            '/auth/reset/<uidb64>/<token>/':
            'users/password_reset_confirm.html',
            '/auth/password_change/': 'users/password_change_form.html',
            '/auth/password_change/done/': 'users/password_change_done.html',
            '/auth/logout/': 'users/logged_out.html',
        }
        for address, template in templates_urls_names.items():
            with self.subTest(address=address):
                responce = self.authorized_client.get(address)
                self.assertTemplateUsed(responce, template)
