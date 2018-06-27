from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from app.models import Artical, Vote
#from core.api import utils

class ArticalAPTTest(APITestCase):
  
  def setUp(self):
    # create test user.
    self.test_user = User.objects.create_user('testuser', 'test@example.com',
                                              'testpassword')

  def test_create_user(self):
    '''
    Ensure we can create a new user and a valid token is created with it.
    '''
    data = {
        'username': 'foobar',
        'email': 'foobar@example.com',
        'password': 'somepassword'
    }

    response = self.client.post(reverse('create-user') , data, format='json')

    # We want to make sure we have two users in the database..
    self.assertEqual(User.objects.count(), 2)
    # And that we're returning a 201 created code.
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

  def test_add_artical(self):
    url = reverse('create-artical')
    data = {'auther': 'testuser', 'title': 'Python Intro',
             'content': '''Python is an interpreted high-level programming
                           language for general-purpose programming.
                           Created by Guido van Rossum and first released in 1991,
                           Python has a design philosophy that emphasizes code
                           readability, notably using significant whitespace. '''
            }
    response = self.client.post(url, data=data, format='json')
    self.assertEqual(Artical.objects.count(), 1)
    self.assertEqual(Artical.objects.first().title, data['title'])

  def test_up_vote(self):
    # Create Artical
    artical_obj = Artical.objects.create(active=True, author=self.test_user,
        title='Django', content='''Django is a free and open-source web framework,
          written in Python, which follows the model-view-template architectural
          pattern.''')
    data = {'artical': artical_obj.id,
            'user': self.test_user.username,
           }
    url = reverse('up-vote', kwargs={'id': artical_obj.id})
    response = self.client.post(url, data, format='json')
    self.assertEqual(Vote.objects.count(), 1)
    self.assertEqual(Vote.objects.first().artical.id, artical_obj.id)


  def test_list_artical(self):
    content_1 = '''Django is a free and open-source web framework, written in
                   Python, which follows the model-view-template architectural
                   pattern.'''
    content_2 = '''Flask is a micro web framework written in Python. It is
                   classified as a microframework because it does not require
                   particular tools or libraries.'''
    url = reverse('list-artical')
    # Create Articals.
    artical_obj_1 = Artical.objects.create(active=True, author=self.test_user,
                                           title='Django', content=content_1)
    artical_obj_2 = Artical.objects.create(active=True, author=self.test_user,
                                           title='Flask', content=content_2)
    # Create Users.
    user_obj_1 = User.objects.create_user('testuser1', 'test1@example.com',
                                          'test1password')
    user_obj_2 = User.objects.create_user('testuser2', 'test2@example.com',
                                          'test2password')
    # Up-Vote Artical
    Vote.objects.create(user=self.test_user, artical=artical_obj_1, up_vote=True)
    Vote.objects.create(user=user_obj_1, artical=artical_obj_1, up_vote=True)
    Vote.objects.create(user=user_obj_2, artical=artical_obj_2, up_vote=True)
    response = self.client.get(url)
    self.assertEqual(response.data[0]['title'], artical_obj_1.title)
    self.assertEqual(response.data[1]['title'], artical_obj_2.title)
