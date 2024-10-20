import logging
from typing import Union

from teams.models import Team, TeamToClue
from teams.scripts.get_team_clues_in_order import get_team_clues_in_order

logger = logging.getLogger(__name__)

def get_next_clue(team: Team) -> Union[TeamToClue, None]:
    '''Get the next clue this team needs to solve, or None if team has solved all clues'''
    team_clues = get_team_clues_in_order(team)
    team_clues = list(filter(lambda team_clue: team_clue.found == False, team_clues))
    return team_clues[0] if len(team_clues) != 0 else None
