from itertools import chain
import logging
from typing import Dict

from django.contrib.auth.models import User

from characters.models import Character
from characters.scripts.character_queries import (
    characters_not_on_a_team,
    characters_on_a_team,
)
from teams.models import Team

logger = logging.getLogger(__name__)

def make_teams() -> Dict[str, int]:
    '''Create the teams by updating the Team database

    When this is called teams will be created according to the following:
        1) Team of two will be created if both Characters have each other listed
        2) Team of two will be created if 2+ Characters have solo not marked
        3) Solo team will be created if solo is marked
        4) Solo team will be created if only 1 remaining Character has solo not marked

    Returns:
        Number of teams added to the Team database in the following format:
            {
                'solo': #,
                'duo': #
            }
    '''
    logger.info('Team Creation')
    teams_created = {'solo': 0, 'duo': 0}

    # 1) Team of two will be created if both Characters have each other listed
    logger.info('Making preferred partner teams')
    teams_created = __make_preferred_partner_teams(teams_created)

    # 2) Team of two will be created if 2+ Characters have solo not marked
    teams_created = __make_random_teams(teams_created)
    # 3) Solo team will be created if solo is marked
    # 4) Solo team will be created if only 1 remaining Character has solo not marked
    teams_created = __add_unteamed_characters_to_a_team(teams_created)

    return teams_created


def __make_random_teams(teams_created: Dict[str, int]) -> Dict[str, int]:
    '''Adds characters who are not on a team nor marked solo to a team

    Teams will be matched according to their past/future preferences. If there is a mismatch
    in number of past/future preferences, remaining characters will be randomly assigned
    against their preference.

    Args:
        teams_created: Dict of {'solo': #, 'duo': #} Representing the number of solo vs duo teams

    Returns:
        Updated teams_created dict
    '''
    chars_not_on_a_team = characters_not_on_a_team().filter(solo=False)

    # Don't re-process characters once they've been added to a team
    characters_added_to_a_team = set()

    past_preferred_chars = chars_not_on_a_team.filter(past_or_future='p')
    future_preferred_chars = chars_not_on_a_team.filter(past_or_future='f')

    def make_team(past_char, future_char):
        '''Creates a team from the past_char and future_char
        Updates teams_created and characters_added_to_a_team
        '''
        team = Team(past_character=past_char, future_character=future_char)
        team.save()
        teams_created['duo'] += 1
        logger.info(f'Adding {past_char.real_name}(p) and {future_char.real_name}(f) to a team')

        # Keep track of which characters are now on a team
        characters_added_to_a_team.add(past_char)
        characters_added_to_a_team.add(future_char)

    # Add past/future preferred characters to their preferred team role until we run out of pairs
    for past_char, future_char in zip(past_preferred_chars, future_preferred_chars):
        make_team(past_char, future_char)

    # Add remaining characters to a team by randomly switching some of their sides
    remaining_chars = list(set(chain(past_preferred_chars, future_preferred_chars)).difference(characters_added_to_a_team))
    for past_char, future_char in zip(remaining_chars[::2], remaining_chars[1::2]):
        if future_char is None:
            continue
        # Update past vs future
        if past_char.past_or_future != 'p':
            Character.objects.filter(id=past_char.id).update(past_or_future='p')
            logger.info(f'Changed {past_char.real_name} from future to past')
        if future_char.past_or_future != 'f':
            Character.objects.filter(id=future_char.id).update(past_or_future='f')
            logger.info(f'Changed {past_char.real_name} from past to future')
        # Make team
        make_team(past_char, future_char)

    return teams_created


def __make_preferred_partner_teams(teams_created: Dict[str, int]) -> Dict[str, int]:
    '''Adds characters who have each other listed as preferred partners to the same team

    If both partners list the same past_or_future preference, they will be randomly assigned
    as either the past or future character

    Args:
        teams_created: Dict of {'solo': #, 'duo': #} Representing the number of solo vs duo teams

    Returns:
        Updated teams_created dict
    '''
    chars_not_on_a_team = characters_not_on_a_team()

    chars_with_prefered_partners = chars_not_on_a_team.filter(preferred_partner__isnull=False)

    # Don't re-process characters once they've been added to a team
    characters_added_to_a_team = set()

    for character in chars_with_prefered_partners:
        if character not in characters_added_to_a_team:
            preferred_partner_character = Character.objects.filter(username=character.preferred_partner).first()
            if not preferred_partner_character:
                return teams_created

            # We already know that character.preferred_partner == preferred_partner_character.username,
            # now we need to check the reverse
            if preferred_partner_character.preferred_partner == character.username:
                # Figure out which time each character should be
                past_char = character
                future_char = preferred_partner_character
                if past_char.past_or_future == 'f':
                    past_char, future_char = future_char, past_char
                # Add characters to a team
                team = Team(past_character=past_char, future_character=future_char)
                team.save()
                teams_created['duo'] += 1
                logger.info(f'Adding {past_char.real_name}(p) and {future_char.real_name}(f) to a preferred partner team')

                # Keep track of which characters are now on a team
                characters_added_to_a_team.add(character)
                characters_added_to_a_team.add(preferred_partner_character)

    return teams_created


def __add_unteamed_characters_to_a_team(teams_created: Dict[str, int]) -> Dict[str, int]:
    '''Adds all characters not currently on a team to a solo team

    Character's past or future preference will be represented on the team

    Args:
        teams_created: Dict of {'solo': #, 'duo': #} Representing the number of solo vs duo teams

    Returns:
        Updated teams_created dict
    '''
    for char_to_add_to_team in characters_not_on_a_team():
        if char_to_add_to_team.past_or_future == 'p':
            team = Team(past_character=char_to_add_to_team)
            logger.info(f'Adding {char_to_add_to_team.real_name} to a team as the past character')
        else:
            team = Team(future_character=char_to_add_to_team)
            logger.info(f'Adding {char_to_add_to_team.real_name} to a team as the future character')
        team.save()
        teams_created['solo'] += 1

    return teams_created
