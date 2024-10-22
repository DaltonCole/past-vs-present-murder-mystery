import logging

from django.http import HttpResponse
from django.shortcuts import render

from characters.models import Character
from pages.scripts.team_to_clue_to_clue_context import team_to_clue_to_clue_context
from teams.scripts.get_next_clue import get_next_clue
from teams.scripts.get_team import get_team

logger = logging.getLogger(__name__)

# Create your views here.
def clue_hint(request):
    character = Character.objects.get(username=request.user.id)
    team = get_team(character)
    clue = get_next_clue(team)
    clue.location_hints += 1
    clue.save()
    logger.info(f'Team({team}) used {clue.location_hints} hints!')

    context = team_to_clue_to_clue_context(clue)

    hint = context['hint2'] if clue.location_hints == 1 else context['hint3']

    return HttpResponse(f'Hint {clue.location_hints + 1}: {hint}')
