import logging

from admin_pages.scripts.assign_clues_to_teams import assign_clues_to_teams
from admin_pages.tests.test_scripts import MakeTeams
from bonus_points.models import BonusPoint
from bonus_points.scripts.assign_bonus_points_to_team import assign_bonus_points_to_team
from pages.scripts.calculate_team_score import POINTS_PER_CLUE, calculate_team_score
from teams.models import Team
from teams.scripts.get_team_clues_in_order import get_team_clues_in_order

# Create your tests here.
logging.basicConfig(level=logging.INFO)

class CalculateTeamScoreTests(MakeTeams):
    fixtures = ['fixtures/bonus_points.json',
                'fixtures/descriptor_flavor_text.json',
                'fixtures/occupation_flavor_text.json',
                'fixtures/story_text_clue.json',
                'fixtures/video_clues.json',
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


    def test_calculate_team_score_clues_plus_bonus_points(self):
        '''Teams have both clues and bonus points'''
        with self.assertLogs(level='INFO') as _:
            team = Team.objects.all()[0]
            team_clues = get_team_clues_in_order(team)
            bonus_points = BonusPoint.objects.all()

            expected_total_points = 0

            # Add clue
            team_clues[0].found = True
            team_clues[0].save()
            expected_total_points += POINTS_PER_CLUE
            points, _ = calculate_team_score(team)
            self.assertEqual(points, expected_total_points)
            # Add clue
            team_clues[1].found = True
            team_clues[1].save()
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
            team_clues[2].found = True
            team_clues[2].save()
            expected_total_points += POINTS_PER_CLUE
            points, _ = calculate_team_score(team)
            self.assertEqual(points, expected_total_points)
