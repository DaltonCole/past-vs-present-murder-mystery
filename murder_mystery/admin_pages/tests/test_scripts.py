from django.test import TestCase
from django.contrib.auth.models import User
import logging

from characters.models import Character
from teams.models import Team
from admin_pages.scripts.make_teams import make_teams
from .helpers import save_all, make_default_character

# Create your tests here.
logging.basicConfig(level=logging.INFO)


class MakeTeamsTests(TestCase):
    def test_team_already_exists(self):
        '''Make sure characters already on a team aren't added to another team'''
        # Create 10 users
        users = [User(username=num) for num in range(10)]
        save_all(users)
        # Create 10 characters
        chars = [make_default_character(user) for user in users]

        # Update characters so 2 are the past character and 1 is a future character
        chars[3].real_name = 'bob'
        chars[4].real_name = 'charlie'
        chars[4].past_or_future = 'f'
        chars[2].solo = True
        chars[3].solo = True
        chars[4].solo = True

        # Create a single team
        save_all(chars) # Save final chars
        team1 = Team(past_character=chars[0], future_character=chars[1])
        team2 = Team(past_character=chars[2])
        team1.save()
        team2.save()

        # Make teams
        with self.assertLogs(level='INFO') as lc:
            teams_created = make_teams()

            # Verify the correct characters were added to a team
            self.assertIn('Adding bob to a team as the past character', '\t'.join(lc.output))
            self.assertIn('Adding charlie to a team as the future character', '\t'.join(lc.output))

        # Verify 4 teams were created
        self.assertEqual(7, len(Team.objects.all()))

        self.assertDictEqual(
            {'solo': 3, 'duo': 2},
            teams_created
        )

    def test_case_1_make_preferred_partner_teams(self):
        '''Preferred partner teams are created correctly
        '''
        # Create 3 users
        users = [User(username=num) for num in range(3)]
        save_all(users)
        # Create 3 characters
        chars = [make_default_character(user) for user in users]

        # Update characters so 2 are the past character and 1 is a future character
        chars[0].preferred_partner = users[2]
        chars[1].preferred_partner = users[2]
        chars[2].preferred_partner = users[1]
        chars[0].real_name = 'alex'
        chars[1].real_name = 'bob'
        chars[2].real_name = 'charlie'
        chars[1].past_or_future = 'f'
        chars[2].past_or_future = 'p'
        save_all(chars) # Save final chars

        # Make teams
        with self.assertLogs(level='INFO') as lc:
            teams_created = make_teams()

            # Verify the correct characters were added to a team
            self.assertIn('Adding charlie(p) and bob(f) to a preferred partner team', '\t'.join(lc.output))

        # Verify 2 teams were created
        self.assertEqual(2, len(Team.objects.all()))

        self.assertDictEqual(
            {'solo': 1, 'duo': 1},
            teams_created
        )

    def test_case_2_not_solo_nor_preferred_teams(self):
        '''Teams of two are created for those not marked as solo
        '''
        # Create 9 users
        users = [User(username=num) for num in range(9)]
        save_all(users)
        # Create 9 characters
        chars = [make_default_character(user) for user in users]

        # Update characters so 2 are the past characters
        chars[0].past_or_future = 'f'
        chars[1].past_or_future = 'f'
        chars[0].real_name = 'alex'
        chars[1].real_name = 'bob'
        save_all(chars) # Save final chars

        # Make teams
        with self.assertLogs(level='INFO') as lc:
            teams_created = make_teams()

            # Verify the correct characters were added to a team
            self.assertIn(' and alex(f) to a team', '\t'.join(lc.output))
            self.assertIn(' and bob(f) to a team', '\t'.join(lc.output))
            self.assertIn(' from past to future', '\t'.join(lc.output))
            self.assertNotIn(' from future to past', '\t'.join(lc.output))

        # Verify 2 teams were created
        self.assertEqual(5, len(Team.objects.all()))

        self.assertDictEqual(
            {'solo': 1, 'duo': 4},
            teams_created
        )

    def test_case_3_solo_prefered(self):
        '''Teams marked as solo are on a solo team
        '''
        # Create 5 users
        users = [User(username=num) for num in range(5)]
        save_all(users)
        # Create 5 characters
        chars = [make_default_character(user) for user in users]

        # Update characters so 2 are the past character and 1 is a future character
        chars[4].past_or_future = 'f'
        chars[2].real_name = 'alex'
        chars[3].real_name = 'bob'
        chars[4].real_name = 'charlie'
        chars[2].solo = True
        chars[3].solo = True
        chars[4].solo = True
        save_all(chars)

        # Make teams
        with self.assertLogs(level='INFO') as lc:
            teams_created = make_teams()

            # Verify the correct characters were added to a team
            self.assertIn('Adding alex to a team as the past character', '\t'.join(lc.output))
            self.assertIn('Adding bob to a team as the past character', '\t'.join(lc.output))
            self.assertIn('Adding charlie to a team as the future character', '\t'.join(lc.output))

        # Verify 4 teams were created
        self.assertEqual(4, len(Team.objects.all()))

        self.assertDictEqual(
            {'solo': 3, 'duo': 1},
            teams_created
        )

