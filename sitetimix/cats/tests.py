from http import HTTPStatus
from django.test import TestCase
from django.urls import reverse

from cats.models import Cat

# Create your tests here.
class GetPagesTestCase(TestCase):
    fixtures = [
        'cat_cat.json',
        'cat_owner.json',
        'cat_species.json',
        'cat_tagpost.json',
    ]
    
    def setUp(self):
        '''Inits tests'''

    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('cats/index.html', response.template_name)
        self.assertTemplateUsed(response, 'cats/index.html')
        self.assertEqual(response.context_data["title"], "Главная страница")
    
    def test_redirect_addpage(self):
        path = reverse('add_page')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)
    
    def test_data_mainpage(self):
        cat_data = Cat.published.all().select_related('spec')
        path = reverse('home')
        response = self.client.get(path)
        self.assertQuerysetEqual(response.context_data['posts'], cat_data[:5])
        
    def test_paginate_mainpage(self):
        path = reverse('home')
        page = 2
        paginate_by = 5
        response = self.client.get(path + f'?page={page}')
        cat_data = Cat.published.all().select_related('spec')
        self.assertQuerysetEqual(response.context_data['posts'], cat_data[(page-1) * paginate_by : page * paginate_by])
        
    def test_content_post(self):
        cat_first = Cat.published.get(pk=1)
        path = reverse('post', args=[cat_first.slug])
        response = self.client.get(path)
        self.assertEqual(cat_first.content, response.context_data['post'].content)
        
    def tearDown(self):
        '''End tests'''