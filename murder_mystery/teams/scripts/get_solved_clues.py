import logging
from typing import List

from teams.models import Team, TeamToClue
from teams.scripts.get_team_clues_in_order import get_team_clues_in_order

logger = logging.getLogger(__name__)

def get_solved_clues(team: Team) -> List[TeamToClue]:
    '''Get the clues this team has already solved'''
    return list(TeamToClue.objects.filter(team=team, found=True).order_by('order'))
