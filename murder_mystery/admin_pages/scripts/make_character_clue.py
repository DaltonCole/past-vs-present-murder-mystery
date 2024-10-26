from itertools import chain, zip_longest
import logging
from random import shuffle
from typing import Dict, List, Tuple, Union

from django.contrib.auth.models import User

from character_clues.models import (
    CharacterClue,
    DescriptorFlavorText,
    OccupationFlavorText,
    StoryClue,
)
from characters.models import Character
from characters.models import Character
from characters.scripts.character_queries import (
    characters_not_on_a_team,
    characters_on_a_team,
)
from location_clues.models import LocationClue
from teams.models import Team, TeamToClue

logger = logging.getLogger(__name__)


def make_character_clue(story_clue: StoryClue, character: Character) -> CharacterClue:
    '''Create a character clue and save it to the database

    Args:
        story_clue: StoryClue to relate the created character clue to
        character: Character to assign to this clue

    Raises:
        ValueError: No OccupationFlavorTexts found in the db
        ValueError: Less than 3 DescriptorFlavorTexts found in the db

    Returns:
        The generated character clue
    '''
    occupation_options = list(OccupationFlavorText.objects.all())
    descriptor_options = list(DescriptorFlavorText.objects.all())
    shuffle(occupation_options)
    shuffle(descriptor_options)

    if len(occupation_options) == 0:
        raise ValueError('No occupation flavor characters in the database.')
    if len(descriptor_options) < 3:
        raise ValueError(f'Not enough descriptor flavor characters in the database. Found {len(descriptor_options)} but require 3')

    character_clue = CharacterClue(
            story_clue=story_clue,
            character_id=character,
            occupation_flavor_text=occupation_options[0],
            descriptor1_flavor_text=descriptor_options[0],
            descriptor2_flavor_text=descriptor_options[1],
            descriptor3_flavor_text=descriptor_options[2],
            )
    character_clue.save()

    return character_clue
