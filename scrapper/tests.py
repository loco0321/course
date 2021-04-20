from django.contrib.auth.models import User
from django.test import TestCase
from scrapper.models import Movie


# Create your tests here.

class AuthTestCase(TestCase):

    def setUp(self):
        user, created = User.objects.update_or_create(username='leon', email='leon@gmail.com', is_superuser=True)
        user.set_password('leon')
        user.is_staff = True
        user.is_active = True
        user.save()

    def test_access_admin(self):
        response = self.client.get('/admin/auth/user/')
        self.assertRedirects(response, '/admin/login/?next=/admin/auth/user/')
        self.client.login(**{'username': 'leon', 'password': 'leon'})
        response = self.client.get('/admin/auth/user/')
        self.assertEqual(200, response.status_code)


class ModelMovieTestCase(TestCase):

    def setUp(self):
        movie = Movie.objects.create(name='nose')

    def test_number_of_movies(self):
        count = Movie.objects.count()
        self.assertEqual(1, count)

    def test_str(self):
        movie = Movie.objects.last()
        self.assertEqual('nose', str(movie))

    def test_nose(self):
        movie = Movie.objects.last()
        self.assertEqual(movie.nose(), 1)
