import logging

from location_clues.models import Location, LocationClue
from story_clues.models import StoryClue

logger = logging.getLogger(__name__)


def make_location_clue(story_clue: StoryClue, location: Location) -> LocationClue:
    '''Create a location clue and save it to the database

    Args:
        story_clue: StoryClue to relate the created location clue to

    Raises:

    Returns:
        The generated location clue
    '''

    location_clue = LocationClue(
            story_clue=story_clue,
            location=location
            )
    location_clue.save()

    return location_clue
