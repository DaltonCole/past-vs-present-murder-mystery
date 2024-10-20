from django.test import TestCase
import logging

from teams.models import Team
from admin_pages.scripts.make_teams import make_teams
from bonus_points.models import BonusPoint, TeamToBonusPoint
from bonus_points.scripts.assign_bonus_points_to_team import assign_bonus_points_to_team
from bonus_points.scripts.get_available_bonus_points import get_available_bonus_points
from bonus_points.scripts.get_team_bonus_points import get_team_bonus_points
from admin_pages.tests.helpers import save_all, make_n_users_and_characters

# Create your tests here.
logging.basicConfig(level=logging.INFO)


class MakeTeams(TestCase):
    fixtures = ['fixtures/bonus_points.json']

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


class GetAvailableBonusPointsTests(MakeTeams):
    def test_get_available_bonus_points(self):
        '''Complete test for get_team_bonus_points'''
        self.make_teams()
        teams = Team.objects.all()
        bonus_points = BonusPoint.objects.all()
        self.assertGreaterEqual(len(bonus_points), 4)
        self.assertEqual(len(get_available_bonus_points()), len(bonus_points))

        for i, bonus_point in enumerate(bonus_points):
            TeamToBonusPoint(team=teams[0], bonus_point=bonus_point).save()
            self.assertEqual(len(get_available_bonus_points()), len(bonus_points) - i - 1)


class AssignBonusPointsToTeamTests(MakeTeams):
    def test_assign_bonus_points_to_team(self):
        '''Complete test for assign_clues_to_teams'''
        self.make_teams()
        teams = Team.objects.all()
        team1 = teams[0]
        bonus_points = BonusPoint.objects.all()
        self.assertGreaterEqual(len(bonus_points), 4)
        with self.assertLogs(level='INFO') as lc:
            # Assign first bonus point to team1
            assign_bonus_points_to_team(team1, bonus_points[0])
            self.assertEqual(len(TeamToBonusPoint.objects.all()), 1)
            self.assertIn(f'Team{team1} has been awarded the bonus point {bonus_points[0]}', '\t'.join(lc.output))
            TeamToBonusPoint.objects.get(team=team1)
            TeamToBonusPoint.objects.get(bonus_point=bonus_points[0])
            # Assign second bonus point to team1
            assign_bonus_points_to_team(team1, bonus_points[1])
            self.assertIn(f'Team{team1} has been awarded the bonus point {bonus_points[1]}', '\t'.join(lc.output))
            self.assertEqual(len(TeamToBonusPoint.objects.all()), 2)
            self.assertEqual(len(TeamToBonusPoint.objects.filter(team=team1)), 2)
            TeamToBonusPoint.objects.filter(bonus_point=bonus_points[1])
            # Assign third bonus point to team2
            team2 = teams[1]
            assign_bonus_points_to_team(team2, bonus_points[2])
            self.assertIn(f'Team{team2} has been awarded the bonus point {bonus_points[2]}', '\t'.join(lc.output))
            self.assertEqual(len(TeamToBonusPoint.objects.all()), 3)
            self.assertEqual(len(TeamToBonusPoint.objects.filter(team=team2)), 1)
            TeamToBonusPoint.objects.filter(bonus_point=bonus_points[2])
            # Assign fourth bonus point to team1
            assign_bonus_points_to_team(team1, bonus_points[3])
            self.assertIn(f'Team{team1} has been awarded the bonus point {bonus_points[3]}', '\t'.join(lc.output))
            self.assertEqual(len(TeamToBonusPoint.objects.all()), 4)
            self.assertEqual(len(TeamToBonusPoint.objects.filter(team=team1)), 3)
            TeamToBonusPoint.objects.filter(bonus_point=bonus_points[3])


class GetTeamBonusPointsTests(MakeTeams):
    def test_get_team_bonus_points(self):
        '''Complete test of get_team_bonus_points'''
        self.make_teams()
        teams = Team.objects.all()
        bonus_points = BonusPoint.objects.all()
        self.assertGreaterEqual(len(bonus_points), 4)

        with self.assertLogs(level='INFO') as lc:
            # Team 0 + bonus points 0
            TeamToBonusPoint(team=teams[0], bonus_point=bonus_points[0]).save()
            points, bonus_list = get_team_bonus_points(teams[0])
            self.assertEqual(points, bonus_points[0].amount)
            self.assertEqual(len(bonus_list), 1)
            self.assertIn(f'Team{teams[0]} has {points} bonus points for [\'{bonus_points[0].reason}\']', '\t'.join(lc.output))

            # Team 1 + bonus points 1
            TeamToBonusPoint(team=teams[1], bonus_point=bonus_points[1]).save()
            points, bonus_list = get_team_bonus_points(teams[1])
            self.assertEqual(points, bonus_points[1].amount)
            self.assertEqual(len(bonus_list), 1)
            self.assertIn(f'Team{teams[1]} has {points} bonus points for [\'{bonus_points[1].reason}\']', '\t'.join(lc.output))

            # Team 0 + bonus points 2
            TeamToBonusPoint(team=teams[0], bonus_point=bonus_points[2]).save()
            points, bonus_list = get_team_bonus_points(teams[0])
            self.assertEqual(points, bonus_points[0].amount + bonus_points[1].amount)
            self.assertEqual(len(bonus_list), 2)
            self.assertIn(f'Team{teams[0]} has {points} bonus points for [\'{bonus_points[0].reason}\', \'{bonus_points[2].reason}\']', '\t'.join(lc.output))
