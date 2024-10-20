import logging
from typing import Tuple, List

from bonus_points.models import BonusPoint, TeamToBonusPoint
from teams.models import Team

logger = logging.getLogger(__name__)

def get_available_bonus_points() -> List[BonusPoint]:
    '''Get all bonus points that have not been assigned to a team

    Returns:
        [Bonus points not assigned to a team]
    '''
    team_to_bonus_points = TeamToBonusPoint.objects.all()
    bonus_point_ids = [team_to_bonus_point.bonus_point.id for team_to_bonus_point in team_to_bonus_points]

    return list(BonusPoint.objects.exclude(id__in=bonus_point_ids))
