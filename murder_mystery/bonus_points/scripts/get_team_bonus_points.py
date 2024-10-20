import logging
from typing import Tuple, List

from bonus_points.models import BonusPoint, TeamToBonusPoint
from teams.models import Team

logger = logging.getLogger(__name__)

def get_team_bonus_points(team: Team) -> Tuple[int, List[BonusPoint]]:
    '''Get all of the bonus points this team has

    Args:
        team: Team to find bonus points for

    Returns:
        (# of points this team has, [Bonus Points associated with this team])
    '''
    team_to_bonus_points = TeamToBonusPoint.objects.filter(team=team)

    total_points = 0
    bonus_points = []

    for team_to_bonus in team_to_bonus_points:
        total_points += team_to_bonus.bonus_point.amount
        bonus_points.append(team_to_bonus.bonus_point)

    logger.info(f'Team{team} has {total_points} bonus points for {[bonus_point.reason for bonus_point in bonus_points]}')

    return (total_points, bonus_points)
