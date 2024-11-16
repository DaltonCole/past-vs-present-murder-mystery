import logging
from typing import Dict, List, Union

from admin_pages.scripts.assign_clues_to_teams import assign_clues_to_teams
from admin_pages.scripts.make_teams import make_teams
from teams.models import Team, TeamToClue

logger = logging.getLogger(__name__)
def start_game() -> Dict[str, Union[Dict[str, int], Dict[Team, List[TeamToClue]]]]:
    '''Start the game

    Upon game start, the following will happen:
        1) Each character will be assigned a team
            * I.e. Team db will be populated
        2) Each team will be assigned every clue
            * I.e. TeamToClue db will be populated

    On subsequent calls to this function, the above will be done for new
    characters without affecting existing Characters on a Team

    Returns:
        The Teams db and TeamToClue db will be populated. The number of teams
        and clues added with be given as a python dict in the following format:
        {
            'teams': {'solo': #, 'duo': #}
            'team_to_clues': {Team: List[TeamToClue]}
        }
    '''
    logger.info('Starting Game')
    status_dict = {}
    # Make the teams
    status_dict['teams'] = make_teams()
    # Assign clues to teams
    status_dict['team_to_clues'] = assign_clues_to_teams()
    logger.info(f'The following were added by start_name(): {status_dict}')

    return status_dict


# End the game, do not allow any changes to the Database
def end_game():
    pass
