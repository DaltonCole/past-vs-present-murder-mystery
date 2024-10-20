from typing import Union
import logging


from characters.models import Character
from teams.models import Team

logger = logging.getLogger(__name__)

def get_team(char: Character) -> Union[Team, None]:
    '''Gets the correlated team for a character or None if char is not on a team'''
    past_char = Team.objects.filter(past_character=char)
    if len(past_char) > 0:
        return past_char[0]
    future_char = Team.objects.filter(future_character=char)
    if len(future_char) > 0:
        return future_char[0]
    return None
