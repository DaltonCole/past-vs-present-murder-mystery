from django.shortcuts import reverse
from django.test import TestCase
from django.contrib.auth.models import User
import logging

from characters.models import Character
from teams.models import Team
from .helpers import make_admin_user, make_n_users_and_characters, save_all


# Create your tests here.
logging.basicConfig(level=logging.INFO)

class ViewsTests(TestCase):
    def setUp(self):
        self.user = make_admin_user()
        self.client.force_login(user=self.user)

    def test_start_game(self):
        # TODO
        with self.assertLogs(level='INFO') as lc:
            response = self.client.post(reverse('admin-pages:console'), {'action': 'start-game'}, follow=True)
        # Check status code
        self.assertEqual(response.status_code, 200)

    def test_console_get_team_creation(self):
        users, chars = make_n_users_and_characters(11)
        save_all(users)
        save_all(chars)

        with self.assertLogs(level='INFO') as lc:
            response = self.client.post(reverse('admin-pages:console'), {'action': 'team-creation'}, follow=True)
            # Check status code
            self.assertEqual(response.status_code, 200)

            # Check logs
            self.assertIn('to a team as the past character', '\t'.join(lc.output)) # 1 solo
            self.assertIn('from past to future', '\t'.join(lc.output)) # Change time for chars

        # Verify 6 teams (5 duo, 1 single)
        self.assertEqual(11, len(Character.objects.all()))
        self.assertEqual(6, len(Team.objects.all()))
