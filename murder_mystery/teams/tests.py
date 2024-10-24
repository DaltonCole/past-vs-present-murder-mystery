import logging

from django.test import TestCase
from django.test import TestCase

from admin_pages.scripts.assign_clues_to_teams import assign_clues_to_teams
from admin_pages.scripts.make_teams import make_teams
from admin_pages.tests.helpers import make_n_users_and_characters, save_all
from admin_pages.tests.test_scripts import MakeTeams
from teams.models import Team, TeamToClue
from teams.scripts.get_next_clue import get_next_clue
from teams.scripts.get_solved_clues import get_solved_clues
from teams.scripts.get_team import get_team
from teams.scripts.get_team_clues_in_order import get_team_clues_in_order

# Create your tests here.
logging.basicConfig(level=logging.INFO)

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
        with self.assertLogs(level='INFO') as lc:
            make_teams()
        team = get_team(char)
        self.assertIsNotNone(team)
        past_char = team.past_character
        future_char = team.future_character
        self.assertTrue(char == past_char or char == future_char)
        # Remove teams
        Team.objects.all().delete()
        self.assertIsNone(get_team(char))


class GetTeamCluesInOrderTests(MakeTeams):
    fixtures = ['fixtures/descriptor_flavor_text.json',
                'fixtures/occupation_flavor_text.json',
                'fixtures/story_clue.json',
                'fixtures/location.json',
                ]
    def test_get_team_clues_in_order(self):
        with self.assertLogs(level='INFO') as lc:
            self.make_teams()
            assign_clues_to_teams()
        self.assertGreater(len(Team.objects.all()), 0)
        self.assertGreater(len(TeamToClue.objects.all()), 0)
        for team in Team.objects.all():
            team_clues = get_team_clues_in_order(team)
            for i, team_clue in enumerate(team_clues):
                self.assertEqual(team_clue.order, i + 1)


class GetSolvedCluesTests(MakeTeams):
    fixtures = ['fixtures/descriptor_flavor_text.json',
                'fixtures/occupation_flavor_text.json',
                'fixtures/story_clue.json',
                'fixtures/location.json',
                ]
    def test_get_solved_clues(self):
        with self.assertLogs(level='INFO') as lc:
            self.make_teams()
            assign_clues_to_teams()
        self.assertGreater(len(Team.objects.all()), 0)
        self.assertGreater(len(TeamToClue.objects.all()), 0)
        for team in Team.objects.all():
            team_clues = get_team_clues_in_order(team)
            self.assertEqual(len(get_solved_clues(team)), 0)
            for i, team_clue in enumerate(team_clues):
                team_clue.found = True
                team_clue.save()
                self.assertEqual(len(get_solved_clues(team)), i + 1)


class GetNextClueTests(MakeTeams):
    fixtures = ['fixtures/descriptor_flavor_text.json',
                'fixtures/occupation_flavor_text.json',
                'fixtures/story_clue.json',
                'fixtures/location.json',
                ]
    def test_get_next_clue(self):
        with self.assertLogs(level='INFO') as lc:
            self.make_teams()
            assign_clues_to_teams()
        self.assertGreater(len(Team.objects.all()), 0)
        self.assertGreater(len(TeamToClue.objects.all()), 0)
        for team in Team.objects.all():
            team_clues = get_team_clues_in_order(team)
            for team_clue in team_clues:
                self.assertEqual(get_next_clue(team), team_clue)
                team_clue.found = True
                team_clue.save()
            self.assertIsNone(get_next_clue(team))


