from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from contacts.models import User


# class ContactTests(TestCase):
#
#     def test_str(self):
#         contact = User(first_name='John', last_name='Smith')
#         self.assertEquals(
#             str(contact),
#             'John Smith',
#         )


class UserRegistrationViewTestCase(TestCase):

    def setUp(self):
        self.data = {
            'first_name': 'Max', 'last_name': 'Miller',
            'username': 'maxmill',
            'password1': 'qwer123456'
        }
        self.path = reverse('registration')

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'contacts/registration.html')

    def test_user_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        # check creating of user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username=username).exists())


class UsersViewTestCase(TestCase):

    def test_view(self):
        path = reverse('see_users')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'contacts/users.html')


# class ProfileViewTestCase(TestCase):
#     def setUp(self):
#         self.data = {
#             'username': 'maxmill',
#             'password1': 'qwer123456'
#         }
#
#     def test_view(self):
#         user = User.objects.filter(username=self.data['username'])
#         path = reverse('profile')
#         response = user.get(path)
#
#         self.assertEqual(response.status_code, HTTPStatus.OK)
#         self.assertTemplateUsed(response, 'contacts/profile.html')
