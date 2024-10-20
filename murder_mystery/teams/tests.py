from django.test import TestCase

from teams.scripts.get_team import get_team
from characters.models import Character
from teams.models import Team
from admin_pages.tests.helpers import make_n_users_and_characters, save_all
from admin_pages.scripts.make_teams import make_teams

# Create your tests here.
class GetTeamTests(TestCase):
    def test_get_team(self):
        '''Make sure we can get the team for a character'''
        # Make characters
        users, chars = make_n_users_and_characters(3)
        save_all(users)
        save_all(chars)
        char = chars[0]
        # Team does not exist yet
        self.assertIsNone(get_team(char))
        # Make teams - get_team should return a team
        make_teams()
        team = get_team(char)
        self.assertIsNotNone(team)
        past_char = team.past_character
        future_char = team.future_character
        self.assertTrue(char == past_char or char == future_char)
        # Remove teams
        Team.objects.all().delete()
        self.assertIsNone(get_team(char))
