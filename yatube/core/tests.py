from django.test import TestCase


class StaticPagesURLTests(TestCase):
    def test_core_url_uses_correct_template(self):
        """Проверка шаблонов для адресов приложения core."""
        templates_urls_names = {
            '/unexisting-page/': 'core/404.html',
        }
        for address, template in templates_urls_names.items():
            with self.subTest(address=address):
                response = self.client.get(address)
                self.assertTemplateUsed(response, template)
