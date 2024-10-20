import logging
from typing import List, Tuple

from bonus_points.models import BonusPoint, TeamToBonusPoint
from bonus_points.scripts.get_team_bonus_points import get_team_bonus_points
from teams.models import Team
from teams.scripts.get_team_clues_in_order import get_team_clues_in_order

logger = logging.getLogger(__name__)

POINTS_PER_CLUE = 50

def calculate_team_score(team: Team) -> Tuple[int, List[Tuple[int, str]]]:
    '''Get the total score for this team and the reason behind it

    Args:
        team: Team calculate the score for

    Returns:
        (# of points this team has,
        [(points, "Reason for the points")]
        )
    '''
    total_points = 0
    reasons = []

    # --- Clue points --- #
    team_clues = get_team_clues_in_order(team)

    # For each found clue
    for i, team_clue in enumerate(filter(lambda team_clue: team_clue.found, team_clues)):
        total_points += POINTS_PER_CLUE
        reasons.append((POINTS_PER_CLUE, f'Found clue #{i + 1}'))

    # --- Bonus points --- #
    _, team_bonus_points = get_team_bonus_points(team)

    for bonus_point in team_bonus_points:
        total_points += bonus_point.amount
        reasons.append((bonus_point.amount, bonus_point.reason))

    return (total_points, reasons)
