import logging

from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase

from admin_pages.scripts.make_teams import make_teams
from admin_pages.tests.helpers import (
    make_admin_user,
    make_n_users_and_characters,
    save_all,
)
from admin_pages.tests.test_scripts import MakeTeams
from characters.models import Character
from teams.models import Team


# Create your tests here.
logging.basicConfig(level=logging.INFO)

ALL_FIXTURES = ['fixtures/bonus_points.json',
                'fixtures/descriptor_flavor_text.json',
                'fixtures/occupation_flavor_text.json',
                'fixtures/story_clue.json',
                'fixtures/location.json',
                ]

class HomePreGameTests(TestCase):
    fixtures = ALL_FIXTURES

    def setUp(self):
        self.reverse = reverse('pages:home')

    def test_signup_page_redirect(self):
        '''Assert if not logged in, go to signup page'''
        response = self.client.get(self.reverse, follow=True)
        self.assertRedirects(response, '/accounts/signup/?next=%2F')

    def test_character_creation_redirect(self):
        '''Assert user with no character redirects to character creation screen'''
        user = User(username=1, password='')
        user.save()
        self.client.force_login(user=user)
        response = self.client.get(self.reverse, follow=True)
        self.assertRedirects(response, reverse('characters:creation'))

    def test_waiting_for_game(self):
        '''If user has a character but no team, they should see the waiting for game to start page'''
        user = User(username=1, password='')
        user.save()
        self.client.force_login(user=user)
        char = Character(username=user, solo=False)
        char.save()
        self.assertEqual(len(Team.objects.all()), 0)
        response = self.client.get(self.reverse, follow=True)
        self.assertTemplateUsed(response, 'pages/game-has-not-started.html')


class HomeDuringGameTests(MakeTeams):
    fixtures = ALL_FIXTURES

    def setUp(self):
        self.make_teams()
        self.user = User.objects.all()[0]
        self.char = Character.objects.get(username=self.user)
        self.reverse = reverse('pages:home')
        self.client.force_login(user=self.user)

    def tearDown(self):
        self.assertTemplateNotUsed(self.response, 'pages/game-has-not-started.html')

    def test_context(self):
        '''Verify context'''
        # TODO
        self.response = self.client.post(self.reverse, {'action': 'start-game'}, follow=True)
        # Check status code
        self.assertEqual(self.response.status_code, 200)

