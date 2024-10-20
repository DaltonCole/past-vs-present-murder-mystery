from typing import List
import logging

from teams.models import Team, TeamToClue

logger = logging.getLogger(__name__)

def get_team_clues_in_order(team: Team) -> List[TeamToClue]:
    '''Get the clues associated with this team in order'''
    team_clues = list(TeamToClue.objects.filter(team=team))
    sorted(team_clues, key=lambda team_clue: team_clue.order)
    return team_clues
