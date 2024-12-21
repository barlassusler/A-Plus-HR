import unittest
from django.test import TestCase
from django.contrib.auth import get_user_model

class UserManagerTestCase(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='test@example.com', password='password')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

if __name__ == '__main__':
    unittest.main()
