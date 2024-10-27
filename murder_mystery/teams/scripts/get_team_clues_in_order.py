import logging
from typing import List

from teams.models import Team, TeamToClue

logger = logging.getLogger(__name__)

def get_team_clues_in_order(team: Team) -> List[TeamToClue]:
    '''Get the clues associated with this team in order'''
    team_clues = TeamToClue.objects.filter(team=team).order_by('order')
    return team_clues
