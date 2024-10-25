from itertools import chain, zip_longest
import logging
from random import shuffle
from typing import Dict, List, Tuple, Union

from django.contrib.auth.models import User

from admin_pages.scripts.make_character_clue import make_character_clue
from admin_pages.scripts.make_location_clue import make_location_clue
from character_clues.models import (
    CharacterClue,
    DescriptorFlavorText,
    OccupationFlavorText,
    StoryClue,
)
from characters.models import Character
from characters.scripts.character_queries import (
    characters_not_on_a_team,
    characters_on_a_team,
)
from location_clues.models import Location, LocationClue
from teams.models import Team, TeamToClue

logger = logging.getLogger(__name__)


def assign_clues_to_teams() -> Dict[Team, List[TeamToClue]]:
    '''Assign every clue to every team

    Every team will be assigned every clue. Teams already with any existing clues will
    not be given more clues.

    Clues will be assigned in alternating order between location and character clues,
    with the majority of either going first.

    Returns:
        Dict mapping teams to the clues that were added in the following format:
        {
            Team: [Clue],
        }

    '''
    logger.info('Assigning clues to teams')
    clues_to_team = {}

    story_clues = StoryClue.objects.all()

    def random_clue_order() -> List[StoryClue]:
        '''Get a random clue order'''
        story_clues_list = list(story_clues)
        shuffle(story_clues_list)
        return story_clues_list

    for team in Team.objects.all():
        # Check to see if this team has already been assigned clues
        if len(TeamToClue.objects.filter(team=team)) > 0:
            logger.info(f'{team} has already been assigned clues, skipping.')
            continue

        clues = random_clue_order()

        # Get random location and character clues
        location_clues = list(Location.objects.all())
        character_options = list(Character.objects.exclude(id__in=[
            team.past_character.id if team.past_character is not None else None,
            team.future_character.id if team.future_character is not None else None]))
        shuffle(location_clues)
        shuffle(character_options)

        for i, clue in enumerate(clues):
            # Order for this clue
            next_order = 1 + len(TeamToClue.objects.filter(team=team))

            # Make location clue
            if i % 2 == 0 or len(character_options) == 0:
                logger.info(f'Assigning {team} location clue {clue}')
                location_clue = make_location_clue(clue, location_clues.pop())
                team_to_clue = TeamToClue(team=team, order=next_order, location_clue=location_clue)
            # Make character clue
            else:
                logger.info(f'Assigning {team} story character clue {clue}')
                character_clue = make_character_clue(clue, character_options.pop())
                team_to_clue = TeamToClue(team=team, order=next_order, character_clue=character_clue)

            # Save
            team_to_clue.save()

            # Add clue to team_to_clue dict
            if team not in clues_to_team:
                clues_to_team[team] = []
            clues_to_team[team].append(team_to_clue)

    # TODO: Add option to skip character clues
    # Add bonus screen when team finishes all clues and final solution allowing them to solve remaining location clues
    return clues_to_team


def team_has_story_clue(team: Team, story_clue: StoryClue) -> Union[TeamToClue, None]:
    '''Check to see if a team has already been assigned this story clue

    Returns:
        If this team already has this story clue assigned, via TeamToClue.character_clue
            or TeamToClue.location_clue, return that TeamToClue,
        If multiple of the same story clues for this team exists, a warning log is given and the
            first result is returned
        None otherwise
    '''
    team_character_clues = TeamToClue.objects.filter(team=team).exclude(character_clue__isnull=True).filter(character_clue__story_clue=story_clue)
    team_location_clues = TeamToClue.objects.filter(team=team).exclude(location_clue__isnull=True).filter(location_clue__story_clue=story_clue)

    team_clues = list(team_character_clues) + list(team_location_clues)

    if len(team_clues) > 1:
        logger.warning(f'{team} has multiple of the same story clue, returning first one')
        return team_clues[0]
    if len(team_clues) == 1:
        return team_clues[0]
    else:
        return None
