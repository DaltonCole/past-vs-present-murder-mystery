from django.test import TestCase
from django.contrib.auth.models import User
import logging

from characters.models import Character
from teams.models import Team, TeamToClue
from video_clues.models import VideoClue
from text_clues.models import TextClue, StoryTextClue
from admin_pages.scripts.assign_clues_to_teams import assign_clues_to_teams, team_has_story_text_clue
from admin_pages.scripts.make_teams import make_teams
from admin_pages.scripts.make_text_clue import make_text_clue
from admin_pages.scripts.start_game import start_game
from .helpers import save_all, make_default_character, make_n_users_and_characters

# Create your tests here.
logging.basicConfig(level=logging.INFO)

class MakeTeams(TestCase):
    def make_teams(self):
        '''Create an initial set of teams
        Users and characters are stored in self.users and self.chars, respectively
        '''
        with self.assertLogs(level='INFO') as lc:
            self.users, self.chars = make_n_users_and_characters(7)
            save_all(self.users)
            save_all(self.chars)
            make_teams()
            self.assertEqual(4, len(Team.objects.all()))

class TeamToClueEndState(TestCase):
    def check_team_to_clue_end_state(self):
        '''Confirm the end state of TeamToClue
        The following checks are performed:
            1) Number of teams, video clues, text clues, and team to clue are greater than 0
            2) There is a mapping from every team to every video + text clue
            3) TeamToClue order for each team goes from 1 to num clues
        '''
        num_video_clues = len(VideoClue.objects.all())
        num_text_clues = len(StoryTextClue.objects.all())
        self.assertGreater(len(Team.objects.all()), 0)
        self.assertGreater(num_video_clues, 0)
        self.assertGreater(num_text_clues, 0)
        self.assertGreater(len(TeamToClue.objects.all()), 0)

        def check_team_to_clue_defaults(team_to_clue, video_clue: bool = False):
            '''Make sure TeamToClue populates the correct default values'''
            self.assertEqual(False, team_to_clue.found)
            self.assertEqual(0, team_to_clue.location_hints)
            self.assertEqual(0, team_to_clue.tries)

            if video_clue:
                self.assertIsNone(team_to_clue.text_clue)
                self.assertIsNotNone(team_to_clue.video_clue)
            else:
                self.assertIsNone(team_to_clue.video_clue)
                self.assertIsNotNone(team_to_clue.text_clue)

        for team in Team.objects.all():
            check_order = set()
            # Make sure every team has every video clue
            for video_clue in VideoClue.objects.all():
                team_to_video_clue = TeamToClue.objects.get(team=team, video_clue=video_clue)
                self.assertNotIn(team_to_video_clue.order, check_order)
                check_order.add(team_to_video_clue.order)
                check_team_to_clue_defaults(team_to_video_clue, video_clue=True)
            # Make sure every team has every text clue
            for story_text_clue in StoryTextClue.objects.all():
                with self.assertNoLogs(level='WARNING') as _:
                    team_to_text_clue = team_has_story_text_clue(team, story_text_clue)
                    self.assertIsNotNone(team_to_text_clue)
                self.assertNotIn(team_to_text_clue.order, check_order)
                check_order.add(team_to_text_clue.order)
                check_team_to_clue_defaults(team_to_text_clue, video_clue=False)
            # Make sure order is from 1-num clues
            num_clues = num_video_clues + num_text_clues
            self.assertEqual(num_clues, len(check_order))
            for i in range(1, num_clues + 1):
                self.assertIn(i, check_order)
            # Make sure video + text clue order is alternating
            team_clues = TeamToClue.objects.all().filter(team=team)
            video_clues_order = []
            text_clues_order = []
            for team_clue in team_clues:
                if team_clue.video_clue is not None:
                    video_clues_order.append(team_clue.order)
                else:
                    text_clues_order.append(team_clue.order)
            sorted(video_clues_order)
            sorted(text_clues_order)
            iter = zip(video_clues_order, text_clues_order) if 1 in video_clues_order \
                    else zip(text_clues_order, video_clues_order)
            for clue1, clue2 in iter:
                self.assertEqual(clue1+1, clue2, f'Clue types are not alternating. Video clue order: {video_clues_order}, text clue order: {text_clues_order}')


class MakeTextClue(MakeTeams):
    # Since we are loading our actual flavor texts, no ValueErrors should be given
    # by make_text_clue()
    fixtures = ['fixtures/descriptor_flavor_text.json',
                'fixtures/occupation_flavor_text.json',
                'fixtures/story_text_clue.json',
                ]


    def text_clue_validation(self):
        '''Test all text clues for individual descriptor uniqueness and not none ness'''
        self.assertGreater(len(TextClue.objects.all()), 0)
        for text_clue in TextClue.objects.all():
            # Test not null for all fields
            self.assertIsNotNone(text_clue.story_clue)
            self.assertIsNotNone(text_clue.character_id)
            self.assertIsNotNone(text_clue.occupation_flavor_text)
            self.assertIsNotNone(text_clue.descriptor1_flavor_text)
            self.assertIsNotNone(text_clue.descriptor2_flavor_text)
            self.assertIsNotNone(text_clue.descriptor3_flavor_text)
            # Make sure each descriptor_flavor_text is different
            des_text = set()
            des_text.add(text_clue.descriptor1_flavor_text)
            des_text.add(text_clue.descriptor2_flavor_text)
            des_text.add(text_clue.descriptor3_flavor_text)
            self.assertEqual(len(des_text), 3)

    def test_single_text_clue(self):
        '''Test the creation of a single text clue'''
        self.make_teams()
        team = Team.objects.all()[0]
        story_clue = StoryTextClue.objects.all()[0]
        make_text_clue(story_clue, team)
        self.text_clue_validation()

    def test_many_text_clues(self):
        '''Test creating multiple text clues'''
        self.make_teams()
        team = Team.objects.all()[0]
        for story_clue in StoryTextClue.objects.all():
            make_text_clue(story_clue, team)
        self.text_clue_validation()


class TeamHasStoryTextClueTests(MakeTeams):
    fixtures = ['fixtures/descriptor_flavor_text.json',
                'fixtures/occupation_flavor_text.json',
                'fixtures/story_text_clue.json',
                'fixtures/video_clues.json',
                ]

    def setUp(self):
        self.make_teams()
        self.team = Team.objects.all()[0]
        self.story_clue = StoryTextClue.objects.all()[0]
        self.text_clue = make_text_clue(self.story_clue, self.team)

    def test_team_has_story_text_clue(self):
        '''Confirm team has story test clue'''
        team_to_clue = TeamToClue(
                team=self.team,
                text_clue=self.text_clue,
                order=1,
                )
        team_to_clue.save()

        with self.assertNoLogs(level='WARNING') as _:
            self.assertEqual(team_has_story_text_clue(self.team, self.story_clue), team_to_clue)

    def test_team_has_multiple_of_the_same_story_text_clue(self):
        '''Confirm WARNING log is given if team has multiple of the same story text clue'''
        team_to_clue = TeamToClue(
                team=self.team,
                text_clue=self.text_clue,
                order=1,
                )
        team_to_clue.save()
        team_to_clue2 = TeamToClue(
                team=self.team,
                text_clue=self.text_clue,
                order=1,
                )
        team_to_clue2.save()

        with self.assertLogs(level='WARNING') as lc:
            self.assertEqual(team_has_story_text_clue(self.team, self.story_clue), team_to_clue)
            self.assertIn('has multiple of the same story clue, returning first one', '\t'.join(lc.output))

    def test_team_does_not_have_story_text_clue(self):
        '''Confirm team does not have story test clue'''
        self.assertIsNone(team_has_story_text_clue(self.team, self.story_clue))


class AssignCluesToTeamsTests(MakeTeams, TeamToClueEndState):
    fixtures = ['fixtures/descriptor_flavor_text.json',
                'fixtures/occupation_flavor_text.json',
                'fixtures/story_text_clue.json',
                'fixtures/video_clues.json',
                ]

    def test_add_inital_team_to_clues(self):
        '''Test first call to assign_clues_to_teams
        All teams should be assigned all clues
        '''
        self.make_teams()
        with self.assertLogs(level='INFO') as lc:
            clues_to_teams = assign_clues_to_teams()
        self.check_team_to_clue_end_state()

    def test_teams_added_since_inital_call(self):
        '''Test adding clues to only new teams and not existing teams
        This assumes new clues do not exist
        '''
        self.test_add_inital_team_to_clues()
        # Add more teams
        with self.assertLogs(level='INFO') as lc:
            more_users, more_chars = make_n_users_and_characters(14)
            more_users = more_users[7:]
            more_chars = more_chars[7:]
            save_all(more_users)
            save_all(more_chars)
            make_teams()
            self.assertEqual(len(Team.objects.all()), 8)
        # Check
        with self.assertLogs(level='INFO') as lc:
            clues_to_teams = assign_clues_to_teams()
            self.assertIn('has already been assigned clues, skipping', '\t'.join(lc.output))
            self.assertIn('video clue', '\t'.join(lc.output))
            self.assertIn('story text clue', '\t'.join(lc.output))
        self.check_team_to_clue_end_state()

    def test_no_clues(self):
        '''Insure nothing breaks when no clues exist'''
        self.make_teams()
        VideoClue.objects.all().delete()
        StoryTextClue.objects.all().delete()
        with self.assertLogs(level='INFO') as lc:
            clues_to_teams = assign_clues_to_teams()
        self.assertEqual(len(TeamToClue.objects.all()), 0)
        self.assertEqual(len(clues_to_teams), 0)

    def test_no_teams(self):
        '''Insure nothing breaks when no teams exist'''
        with self.assertLogs(level='INFO') as lc:
            clues_to_teams = assign_clues_to_teams()
        self.assertEqual(len(clues_to_teams), 0)
        self.assertEqual(len(TeamToClue.objects.all()), 0)

    def test_random_clue_order(self):
        '''Make sure each team has a random ordering of clues'''
        # Make 20 teams to make it very unlikely any team clue order is the same
        with self.assertLogs(level='INFO') as lc:
            self.users, self.chars = make_n_users_and_characters(39)
            save_all(self.users)
            save_all(self.chars)
            make_teams()
            self.assertEqual(20, len(Team.objects.all()))
        with self.assertLogs(level='INFO') as lc:
            clues_to_teams = assign_clues_to_teams()
        self.check_team_to_clue_end_state()
        # Check random order
        clue_order = set()
        for team in Team.objects.all():
            team_to_clues = TeamToClue.objects.filter(team=team)
            this_clue_order = []
            for i in range(1, len(team_to_clues) + 1):
                clue = team_to_clues.get(order=i)
                clue = clue.video_clue if clue.video_clue is not None else clue.text_clue.story_clue
                this_clue_order.append(clue)
            clue_order.add(tuple(this_clue_order))
        self.assertGreater(len(clue_order), 1)


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

class StartGameTests(TeamToClueEndState):
    fixtures = ['fixtures/descriptor_flavor_text.json',
                'fixtures/occupation_flavor_text.json',
                'fixtures/story_text_clue.json',
                'fixtures/video_clues.json',
                ]

    def test_inital_start_game_small(self):
        '''Test calling start_play() once with only 3 players (2 teams)'''
        with self.assertLogs(level='INFO') as lc:
            self.users, self.chars = make_n_users_and_characters(3)
            save_all(self.users)
            save_all(self.chars)
            start_game()
            # Start game logs
            self.assertIn('Starting Game', '\t'.join(lc.output))
            self.assertIn("The following were added by start_name(): {'teams': {'solo': 1, 'duo': 1}, 'team_to_clues': {", '\t'.join(lc.output))
            # Team checks
            self.assertEqual(len(Team.objects.all()), 2)
            # Team to clue checks
            self.check_team_to_clue_end_state()

    def test_inital_start_game_med(self):
        '''Test calling start_play() once with 21 players (11 teams)'''
        with self.assertLogs(level='INFO') as lc:
            self.users, self.chars = make_n_users_and_characters(21)
            save_all(self.users)
            save_all(self.chars)
            start_game()
            # Start game logs
            self.assertIn('Starting Game', '\t'.join(lc.output))
            self.assertIn("The following were added by start_name(): {'teams': {'solo': 1, 'duo': 10}, 'team_to_clues': {", '\t'.join(lc.output))
            # Team checks
            self.assertEqual(len(Team.objects.all()), 11)
            # Team to clue checks
            self.check_team_to_clue_end_state()

    def test_inital_start_game_large(self):
        '''Test calling start_play() once with 101 players (51 teams)'''
        with self.assertLogs(level='INFO') as lc:
            self.users, self.chars = make_n_users_and_characters(101)
            save_all(self.users)
            save_all(self.chars)
            start_game()
            # Start game logs
            self.assertIn('Starting Game', '\t'.join(lc.output))
            self.assertIn("The following were added by start_name(): {'teams': {'solo': 1, 'duo': 50}, 'team_to_clues': {", '\t'.join(lc.output))
            # Team checks
            self.assertEqual(len(Team.objects.all()), 51)
            # Team to clue checks
            self.check_team_to_clue_end_state()

    def test_inital_start_game_large_even(self):
        '''Test calling start_play() once with 100 players (50 teams)'''
        with self.assertLogs(level='INFO') as lc:
            self.users, self.chars = make_n_users_and_characters(100)
            save_all(self.users)
            save_all(self.chars)
            start_game()
            # Start game logs
            self.assertIn('Starting Game', '\t'.join(lc.output))
            self.assertIn("The following were added by start_name(): {'teams': {'solo': 0, 'duo': 50}, 'team_to_clues': {", '\t'.join(lc.output))
            # Team checks
            self.assertEqual(len(Team.objects.all()), 50)
            # Team to clue checks
            self.check_team_to_clue_end_state()

    def test_multiple_start_game_calls(self):
        '''Test calling start_game() multiple times'''
        self.test_inital_start_game_large()
        players = [10, 11, 1, 7, 8, 1, 1, 1]
        teams = [56, 62, 63, 67, 71, 72, 73, 74]
        for additional_players, total_team_count in zip(players, teams):
            with self.assertLogs(level='INFO') as lc:
                self.users, self.chars = make_n_users_and_characters(additional_players)
                save_all(self.users)
                save_all(self.chars)
                start_game()
                # Start game logs
                self.assertIn('Starting Game', '\t'.join(lc.output))
                # Team checks
                self.assertEqual(len(Team.objects.all()), total_team_count)
                # Team to clue checks
                self.check_team_to_clue_end_state()
