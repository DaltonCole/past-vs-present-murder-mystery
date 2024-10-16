from django.shortcuts import reverse
from typing import Dict, Union
from django.test import TestCase
from django.contrib.auth.models import User
import logging

from characters.models import Character
from .forms import CharacterForm


# Create your tests here.
logging.basicConfig(level=logging.INFO)

def get_form_data() -> Dict[str, Union[str, bool]]:
    '''Returns a dictionary of all the data needed for a Character form'''
    return {
            'real_name': 'Bob',
            'character_name': 'Joe',
            'past_or_future': 'p',
            'occupation': 'Sad person',
            'descriptor1': 'Happy',
            'descriptor2': 'Happy',
            'descriptor3': 'Happy',
            'solo': True,
            }

class FormTests(TestCase):
    def login(self) -> User:
        '''Login a normal user and return said user'''
        user = User.objects.create_user(username='testuser', password='')
        self.client.login(username='testuser', password='')
        return user

    def test_successful_form_submission(self):
        user = self.login()
        form_data = get_form_data()
        form = CharacterForm(user_id=user.id, data=form_data)
        self.assertTrue(form.is_valid())

    def test_bad_form_submission(self):
        '''Make sure form is not allowed if not all information is filled out'''
        user = self.login()
        form_data = get_form_data()
        del form_data['real_name']
        form = CharacterForm(user_id=user.id, data=form_data)
        self.assertFormError(form, 'real_name', 'This field is required.')


class CreationViewTests(TestCase):
    def login(self) -> User:
        '''Login a normal user and return said user'''
        user = User.objects.create_user(username='testuser', password='')
        self.client.login(username='testuser', password='')
        return user

    def test_page_200(self):
        '''Make sure if we are logged in, that we get a 200 status code '''
        self.login()
        response = self.client.get(reverse('characters:creation'), follow=True)
        self.assertEqual(200, response.status_code)

    def test_successful_form_submission(self):
        '''Test good form is good'''
        self.login()
        form_data = get_form_data()
        response = self.client.post(reverse('characters:creation'), form_data, follow=True)
        self.assertRedirects(response, reverse('pages:home'))

    def test_incorrect_form_submission(self):
        '''Test form missing field fails'''
        self.login()
        form_data = get_form_data()
        del form_data['real_name']
        response = self.client.post(reverse('characters:creation'), form_data, follow=True)
        self.assertIn('This field is required.', response.context['form'].errors['real_name'])

    def test_redirect_if_user_is_not_logged_in(self):
        '''If we are not logged in, we should redirect'''
        response = self.client.get(reverse('characters:creation'), follow=True)
        # Make sure we redirect
        self.assertRedirects(response, '/accounts/signup/?next=%2Fcharacters%2Fcreation%2F')

    def test_redirect_if_user_already_has_a_character(self):
        '''Make sure we cant go back to the character form if user already has a character'''
        user = self.login()
        char = Character(username=user, solo=False)
        char.save()
        response = self.client.get(reverse('characters:creation'), follow=True)
        # Make sure we redirect
        self.assertRedirects(response, reverse('pages:home'))
