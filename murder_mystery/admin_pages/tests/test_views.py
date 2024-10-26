import logging

from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase

from characters.models import Character
from teams.models import Team

from .helpers import make_admin_user, make_n_users_and_characters, save_all
from .test_scripts import TeamToClueEndState


# Create your tests here.
logging.basicConfig(level=logging.INFO)

class ConsoleTests(TeamToClueEndState):
    fixtures = ['fixtures/descriptor_flavor_text.json',
                'fixtures/occupation_flavor_text.json',
                'fixtures/story_clue.json',
                'fixtures/location.json',
                ]

    def setUp(self):
        self.user = make_admin_user()
        self.client.force_login(user=self.user)
        self.reverse = 'admin-pages:console'

    def test_start_game(self):
        users, chars = make_n_users_and_characters(5)
        save_all(users)
        save_all(chars)
        with self.assertLogs(level='INFO') as lc:
            response = self.client.post(reverse(self.reverse), {'action': 'start-game'}, follow=True)
        # Check status code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Team.objects.all()), 3)
        self.check_team_to_clue_end_state()


class TestConsoleTests(ConsoleTests):
    def setUp(self):
        super().setUp()
        self.reverse = 'admin-pages:test-console'

    def test_add_default_character(self):
        num_users = len(User.objects.all())
        num_chars = len(Character.objects.all())
        response = self.client.post(reverse(self.reverse), {'action': 'add-default-characters'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(User.objects.all()), num_users + 10)
        self.assertEqual(len(Character.objects.all()), num_chars + 10)
