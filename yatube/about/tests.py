from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class StaticPagesURLTests(TestCase):

    def test_about_url_exists_at_desired_location(self):
        """Проверка доступности адресов приложения about."""
        urls = [
            '/about/author/',
            '/about/tech/',
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_url_uses_correct_template(self):
        """Проверка шаблонов для адресов приложения about."""
        templates_urls_names = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }
        for address, template in templates_urls_names.items():
            with self.subTest(address=address):
                response = self.client.get(address)
                self.assertTemplateUsed(response, template)


class StaticViewURLTests(TestCase):

    def test_about_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон.(about)"""
        templates_pages_names = {
            reverse('about:author'): 'about/author.html',
            reverse('about:tech'): 'about/tech.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.client.get(reverse_name)
                self.assertTemplateUsed(response, template)
