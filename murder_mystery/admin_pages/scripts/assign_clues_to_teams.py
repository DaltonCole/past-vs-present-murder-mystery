from typing import Dict, Tuple, List, Union
from random import shuffle
from itertools import chain, zip_longest
import logging

from django.contrib.auth.models import User

from characters.models import Character
from characters.scripts.character_queries import characters_on_a_team, characters_not_on_a_team
from admin_pages.scripts.make_text_clue import make_text_clue
from teams.models import Team, TeamToClue
from video_clues.models import VideoClue
from text_clues.models import TextClue, StoryTextClue, OccupationFlavorText, DescriptorFlavorText

logger = logging.getLogger(__name__)


def assign_clues_to_teams() -> Dict[Team, List[TeamToClue]]:
    '''Assign every clue to every team

    Every team will be assigned every clue. Teams already with any existing clues will
    not be given more clues.

    Clues will be assigned in alternating order between video and text clues,
    with the majority of either going first.

    Returns:
        Dict mapping teams to the clues that were added in the following format:
        {
            Team: [Clue],
        }

    '''
    logger.info('Assigning clues to teams')
    clues_to_team = {}

    video_clues = VideoClue.objects.all()
    story_text_clues = StoryTextClue.objects.all()

    def random_clue_order() -> List[Union[VideoClue, StoryTextClue]]:
        '''Get a random clue order'''
        video_clues_list = list(video_clues)
        story_text_clues_list = list(story_text_clues)
        shuffle(video_clues_list)
        shuffle(story_text_clues_list)
        all_clues = []
        for clue1, clue2 in zip_longest(video_clues_list, story_text_clues_list):
            if len(story_text_clues) > len(video_clues):
                clue1, clue2 = clue2, clue1
            if clue1 is not None:
                all_clues.append(clue1)
            if clue2 is not None:
                all_clues.append(clue2)
        return all_clues

    for team in Team.objects.all():
        # Check to see if this team has already been assigned clues
        if len(TeamToClue.objects.filter(team=team)) > 0:
            logger.info(f'{team} has already been assigned clues, skipping.')
            continue

        clues = random_clue_order()

        for clue in clues:
            # Order for this clue
            next_order = 1 + len(TeamToClue.objects.filter(team=team))

            # Make video clue
            if type(clue) is VideoClue:
                logger.info(f'Assigning {team} video clue {clue}')
                team_to_clue = TeamToClue(team=team, order=next_order, video_clue=clue)
            # Make text clue
            else:
                logger.info(f'Assigning {team} story text clue {clue}')
                text_clue = make_text_clue(clue, team)
                team_to_clue = TeamToClue(team=team, order=next_order, text_clue=text_clue)

            # Save
            team_to_clue.save()

            # Add clue to team_to_clue dict
            if team not in clues_to_team:
                clues_to_team[team] = []
            clues_to_team[team].append(team_to_clue)

    return clues_to_team


def team_has_story_text_clue(team: Team, story_clue: StoryTextClue) -> Union[TeamToClue, None]:
    '''Check to see if a team has already been assigned this story text clue

    Returns:
        If this team already has this story text clue assigned, via TeamToClue.text_clue, return that TeamToClue,
        If multiple of the same story clues for this team exists, a warning log is given and the
            first result is returned
        None otherwise
    '''
    team_text_clues = TeamToClue.objects.filter(team=team).exclude(text_clue__isnull=True).filter(text_clue__story_clue=story_clue)

    if len(team_text_clues) > 1:
        logger.warning(f'{team} has multiple of the same story clue, returning first one')
        return team_text_clues[0]
    if len(team_text_clues) == 1:
        return team_text_clues[0]
    else:
        return None
