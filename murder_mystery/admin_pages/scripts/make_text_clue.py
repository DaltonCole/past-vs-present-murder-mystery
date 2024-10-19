from typing import Dict, Tuple, List, Union
from random import shuffle
from itertools import chain, zip_longest
import logging

from django.contrib.auth.models import User

from characters.models import Character
from characters.scripts.character_queries import characters_on_a_team, characters_not_on_a_team
from teams.models import Team, TeamToClue
from video_clues.models import VideoClue
from text_clues.models import TextClue, StoryTextClue, OccupationFlavorText, DescriptorFlavorText

logger = logging.getLogger(__name__)


def make_text_clue(story_clue: StoryTextClue, team: Team) -> TextClue:
    '''Create a text clue and save it to the database

    Args:
        story_clue: StoryTextClue to relate the created text clue to
        team: Text clue will have a character_id that is not from the team provided

    Raises:
        ValueError: No character not on team found in Character database
        ValueError: No OccupationFlavorTexts found in the db
        ValueError: Less than 3 DescriptorFlavorTexts found in the db

    Returns:
        The generated text clue
    '''
    character_options = list(Character.objects.exclude(id__in=[
        team.past_character.id if team.past_character is not None else None,
        team.future_character.id if team.future_character is not None else None]))
    occupation_options = list(OccupationFlavorText.objects.all())
    descriptor_options = list(DescriptorFlavorText.objects.all())
    shuffle(character_options)
    shuffle(occupation_options)
    shuffle(descriptor_options)

    if len(character_options) == 0:
        raise ValueError('Not enough characters in the database')
    if len(occupation_options) == 0:
        raise ValueError('No occupation flavor texts in the database.')
    if len(descriptor_options) < 3:
        raise ValueError(f'Not enough descriptor flavor texts in the database. Found {len(descriptor_options)} but require 3')

    text_clue = TextClue(
            story_clue=story_clue,
            character_id=character_options[0],
            occupation_flavor_text=occupation_options[0],
            descriptor1_flavor_text=descriptor_options[0],
            descriptor2_flavor_text=descriptor_options[1],
            descriptor3_flavor_text=descriptor_options[2],
            )
    text_clue.save()

    return text_clue
