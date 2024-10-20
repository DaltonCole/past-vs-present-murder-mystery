import logging
from typing import Tuple, List

from bonus_points.models import BonusPoint, TeamToBonusPoint
from teams.models import Team

logger = logging.getLogger(__name__)

def assign_bonus_points_to_team(team: Team, bonus_point: BonusPoint):
    '''Assign this bonus point to this team

    Args:
        team: Team to give bonus point to
        bonus_point: Bonus point to award to this team
    '''
    relation = TeamToBonusPoint(
            team=team,
            bonus_point=bonus_point,
            )
    relation.save()
    logger.info(f'Team{team} has been awarded the bonus point {bonus_point}')
