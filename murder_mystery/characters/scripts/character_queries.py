from typing import Dict, List
from itertools import chain
import logging

from django.contrib.auth.models import User
from django.db.models.query import QuerySet

from characters.models import Character
from teams.models import Team

logger = logging.getLogger(__name__)


def characters_on_a_team() -> QuerySet:
    '''Returns Characters that are currently on a team as neither the past_or_future character'''
    past_chars = Team.objects.filter(past_character__isnull=False).values_list('past_character', flat=True)
    future_chars = Team.objects.filter(future_character__isnull=False).values_list('future_character', flat=True)
    logger.debug(f'Number of past characters found: {len(past_chars)}')
    logger.debug(f'Number of future characters found: {len(future_chars)}')
    chars_on_a_team = list(chain(past_chars, future_chars))
    chars_on_a_team = Character.objects.filter(id__in=chars_on_a_team)
    logger.debug(f'Total number of characters on a team: {len(chars_on_a_team)}')

    return chars_on_a_team


def characters_not_on_a_team() -> QuerySet:
    '''Returns Characters that are currently NOT on a team as neither the past_or_future character'''
    # Get all characters on a team
    chars_on_a_team = characters_on_a_team()

    # Get all characters no on a team
    chars_not_on_a_team = Character.objects.exclude(id__in=chars_on_a_team)
    logger.debug(f'Total number of characters not on a team: {len(chars_not_on_a_team)}')

    return chars_not_on_a_team
