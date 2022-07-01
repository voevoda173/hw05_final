from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..forms import CreationForm

User = get_user_model()


class CreationFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_username')
        cls.form = CreationForm()

    def test_create_new_user(self):
        """При заполнении формы создается новый пользователь."""
        users_count = User.objects.count()
        form_data = {
            'username': 'test_new_username',
            'password1': 'test12345@',
            'password2': 'test12345@',
        }
        self.client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True,
        )
        self.assertEqual(User.objects.count(), users_count + 1)
