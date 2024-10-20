import logging
from typing import List

from teams.models import Team, TeamToClue
from teams.scripts.get_team_clues_in_order import get_team_clues_in_order

logger = logging.getLogger(__name__)

def get_solved_clues(team: Team) -> List[TeamToClue]:
    '''Get the clues this team has already solved'''
    team_clues = get_team_clues_in_order(team)
    team_clues = list(filter(lambda team_clue: team_clue.found == True, team_clues))
    return team_clues
