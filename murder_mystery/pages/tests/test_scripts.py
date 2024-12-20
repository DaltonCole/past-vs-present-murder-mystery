import logging

from admin_pages.scripts.assign_clues_to_teams import assign_clues_to_teams
from admin_pages.scripts.make_character_clue import make_character_clue
from admin_pages.scripts.make_location_clue import make_location_clue
from admin_pages.tests.test_scripts import MakeTeams
from bonus_points.models import BonusPoint
from bonus_points.scripts.assign_bonus_points_to_team import assign_bonus_points_to_team
from characters.models import Character
from location_clues.models import Location, LocationClue
from pages.scripts.calculate_team_score import (
    INCORRECT_GUESS_DEDUCTION,
    POINTS_PER_CLUE,
    calculate_team_score,
)
from pages.scripts.team_to_clue_to_clue_context import team_to_clue_to_clue_context
from story_clues.models import StoryClue
from teams.models import Team, TeamToClue
from teams.scripts.get_team_clues_in_order import get_team_clues_in_order

# Create your tests here.
logging.basicConfig(level=logging.INFO)

class CalculateTeamScoreTests(MakeTeams):
    fixtures = ['fixtures/bonus_points.json',
                'fixtures/descriptor_flavor_text.json',
                'fixtures/occupation_flavor_text.json',
                'fixtures/story_clue.json',
                'fixtures/location.json',
                ]

    def setUp(self):
        with self.assertLogs(level='INFO') as _:
            self.make_teams()
            assign_clues_to_teams()

    def test_calculate_team_score_clues_only(self):
        '''Teams only have clue points'''
        def test_team_clue(team):
            team_clues = get_team_clues_in_order(team)
            self.assertGreaterEqual(len(team_clues), 3)
            for i, team_clue in enumerate(team_clues):
                team_clue.found = True
                team_clue.save()
                score, reasons = calculate_team_score(team)
                self.assertEqual(score, POINTS_PER_CLUE * (i + 1))
                for j, (amount, reason) in enumerate(reasons):
                    self.assertEqual(amount, POINTS_PER_CLUE)
                    self.assertEqual(reason, f'Found clue #{j + 1}')

        teams = Team.objects.all()
        with self.assertLogs(level='INFO') as _:
            for team in teams:
                test_team_clue(team)

    def test_calculate_team_score_bonus_points_only(self):
        '''Teams only have bonus points'''
        def check_score(team, expected_score):
            score, reason = calculate_team_score(team)
            self.assertEqual(score, expected_score)

        with self.assertLogs(level='INFO') as _:
            teams = Team.objects.all()
            bonus_points = BonusPoint.objects.all()
            assign_bonus_points_to_team(teams[0], bonus_points[0])
            check_score(teams[0], bonus_points[0].amount)
            assign_bonus_points_to_team(teams[0], bonus_points[1])
            check_score(teams[0], bonus_points[0].amount + bonus_points[1].amount)
            assign_bonus_points_to_team(teams[1], bonus_points[2])
            check_score(teams[1], bonus_points[2].amount)
            assign_bonus_points_to_team(teams[0], bonus_points[3])
            check_score(teams[0], bonus_points[0].amount + bonus_points[1].amount + bonus_points[3].amount)

    def test_calculate_team_score_negative_points(self):
        '''Team should have negative points due to incorrect clue guesses'''
        with self.assertLogs(level='INFO') as _:
            team = Team.objects.all()[0]
            team_clues = get_team_clues_in_order(team)
            bonus_points = BonusPoint.objects.all()

            expected_total_points = 0

            # Add incorrect clue guess
            TeamToClue.objects.filter(id=team_clues[0].id).update(tries=team_clues[0].tries + 1)
            team_clues = get_team_clues_in_order(team)
            expected_total_points -= INCORRECT_GUESS_DEDUCTION
            points, _ = calculate_team_score(team)
            self.assertEqual(points, expected_total_points)
            self.assertLess(points, 0)
            # Add incorrect clue guess
            TeamToClue.objects.filter(id=team_clues[1].id).update(tries=team_clues[1].tries + 1)
            expected_total_points -= INCORRECT_GUESS_DEDUCTION
            points, _ = calculate_team_score(team)
            self.assertEqual(points, expected_total_points)
            self.assertLess(points, 0)
            # Add clue
            TeamToClue.objects.filter(id=team_clues[1].id).update(found=True)
            expected_total_points += POINTS_PER_CLUE
            points, _ = calculate_team_score(team)
            self.assertEqual(points, expected_total_points)
            # Add bonus
            assign_bonus_points_to_team(team, bonus_points[0])
            expected_total_points += bonus_points[0].amount
            points, _ = calculate_team_score(team)
            self.assertEqual(points, expected_total_points)
            # Add bonus
            assign_bonus_points_to_team(team, bonus_points[1])
            expected_total_points += bonus_points[1].amount
            points, _ = calculate_team_score(team)
            self.assertEqual(points, expected_total_points)
            # Add clue
            TeamToClue.objects.filter(id=team_clues[2].id).update(found=True)
            expected_total_points += POINTS_PER_CLUE
            points, _ = calculate_team_score(team)
            self.assertEqual(points, expected_total_points)

    def test_calculate_team_score_clues_plus_bonus_points(self):
        '''Teams have both clues and bonus points'''
        with self.assertLogs(level='INFO') as _:
            team = Team.objects.all()[0]
            team_clues = get_team_clues_in_order(team)
            bonus_points = BonusPoint.objects.all()

            expected_total_points = 0

            # Add clue
            TeamToClue.objects.filter(id=team_clues[0].id).update(found=True)
            expected_total_points += POINTS_PER_CLUE
            points, _ = calculate_team_score(team)
            self.assertEqual(points, expected_total_points)
            # Add incorrect clue guess
            TeamToClue.objects.filter(id=team_clues[1].id).update(tries=team_clues[1].tries + 1)
            expected_total_points -= INCORRECT_GUESS_DEDUCTION
            points, _ = calculate_team_score(team)
            self.assertEqual(points, expected_total_points)
            # Add incorrect clue guess
            TeamToClue.objects.filter(id=team_clues[1].id).update(tries=team_clues[1].tries + 1)
            expected_total_points -= INCORRECT_GUESS_DEDUCTION
            points, _ = calculate_team_score(team)
            self.assertEqual(points, expected_total_points)
            # Add clue
            TeamToClue.objects.filter(id=team_clues[1].id).update(found=True)
            expected_total_points += POINTS_PER_CLUE
            points, _ = calculate_team_score(team)
            self.assertEqual(points, expected_total_points)
            # Add bonus
            assign_bonus_points_to_team(team, bonus_points[0])
            expected_total_points += bonus_points[0].amount
            points, _ = calculate_team_score(team)
            self.assertEqual(points, expected_total_points)
            # Add bonus
            assign_bonus_points_to_team(team, bonus_points[1])
            expected_total_points += bonus_points[1].amount
            points, _ = calculate_team_score(team)
            self.assertEqual(points, expected_total_points)
            # Add clue
            TeamToClue.objects.filter(id=team_clues[2].id).update(found=True)
            expected_total_points += POINTS_PER_CLUE
            points, _ = calculate_team_score(team)
            self.assertEqual(points, expected_total_points)


class TeamToClueToClueConcharacterTests(MakeTeams):
    fixtures = ['fixtures/bonus_points.json',
                'fixtures/descriptor_flavor_text.json',
                'fixtures/occupation_flavor_text.json',
                'fixtures/story_clue.json',
                'fixtures/location.json',
                ]

    def test_location_clue(self):
        self.make_teams()
        team = Team.objects.all()[0]
        story_clue = StoryClue.objects.all()[0]
        location = Location.objects.get(pk=0)
        location_clue = make_location_clue(story_clue=story_clue, location=location)
        team_to_location_clue = TeamToClue(team=team, order=1, location_clue=location_clue)
        # 1 hint
        clue_context = team_to_clue_to_clue_context(team_to_location_clue)
        self.assertEqual(clue_context['clue-type'], 'location')
        self.assertEqual(clue_context['hint1'], 'Here, we use and store ancient power')
        self.assertEqual(clue_context['hint2'], '')
        self.assertEqual(clue_context['hint3'], '')
        # 1 hint
        team_to_location_clue.location_hints += 1
        team_to_location_clue.save()
        clue_context = team_to_clue_to_clue_context(team_to_location_clue)
        self.assertEqual(clue_context['clue-type'], 'location')
        self.assertEqual(clue_context['hint1'], 'Here, we use and store ancient power')
        self.assertEqual(clue_context['hint2'], 'Vroom Vroom')
        self.assertEqual(clue_context['hint3'], '')
        # 2 hints
        team_to_location_clue.location_hints += 1
        team_to_location_clue.save()
        clue_context = team_to_clue_to_clue_context(team_to_location_clue)
        self.assertEqual(clue_context['clue-type'], 'location')
        self.assertEqual(clue_context['hint1'], 'Here, we use and store ancient power')
        self.assertEqual(clue_context['hint2'], 'Vroom Vroom')
        self.assertEqual(clue_context['hint3'], 'Look up')


    def test_character_clue(self):
        self.make_teams()
        team = Team.objects.all()[0]
        ref_char = Character.objects.all()[3]
        story_clue = StoryClue.objects.all()[0]
        character_clue = make_character_clue(story_clue, ref_char)
        team_to_character_clue = TeamToClue(team=team, order=1, character_clue=character_clue)
        ref_char.occupation = 'Sad person'
        ref_char.descriptor1 = 'Apples'
        ref_char.descriptor2 = 'Banana'
        ref_char.descriptor3 = 'Cake'
        ref_char.save()
        # 1 hint
        clue_context = team_to_clue_to_clue_context(team_to_character_clue)
        self.assertEqual(clue_context['clue-type'], 'person')
        self.assertIn('Apples', clue_context['hint1'])
        self.assertEqual(clue_context['hint2'], '')
        self.assertEqual(clue_context['hint3'], '')
        # 1 hint
        team_to_character_clue.location_hints += 1
        team_to_character_clue.save()
        clue_context = team_to_clue_to_clue_context(team_to_character_clue)
        self.assertEqual(clue_context['clue-type'], 'person')
        self.assertIn('Apples', clue_context['hint1'])
        self.assertIn('Banana', clue_context['hint2'])
        self.assertEqual(clue_context['hint3'], '')
        # 2 hints
        team_to_character_clue.location_hints += 1
        team_to_character_clue.save()
        clue_context = team_to_clue_to_clue_context(team_to_character_clue)
        self.assertEqual(clue_context['clue-type'], 'person')
        self.assertIn('Apples', clue_context['hint1'])
        self.assertIn('Banana', clue_context['hint2'])
        self.assertIn('Cake', clue_context['hint3'])
        self.assertIn('Sad person', clue_context['hint3'])
