from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from characters.models import Character
from pages.scripts.calculate_team_score import calculate_team_score
from pages.scripts.calculate_team_score import HINT_DEDUCTION
from pages.scripts.team_to_clue_to_clue_context import team_to_clue_to_clue_context
from teams.models import Team
from teams.scripts.get_next_clue import get_next_clue
from teams.scripts.get_solved_clues import get_solved_clues
from teams.scripts.get_team import get_team

@login_required(login_url='accounts/signup')
def home(request):
    context = {}
    # Go to character creation screen if no character exists for this user
    try:
        context['character'] = Character.objects.get(username=request.user.id)
    except:
        return redirect('characters:creation')

    # If the game has not started yet, go to the waiting page
    if len(Team.objects.all()) == 0:
        return render(request, 'pages/game-has-not-started.html', context)

    # --- Actions --- #
    if 'action' in request.POST.keys():
        if 'submit-clue' == request.POST['action']:
            # TODO: If guess is correct, do not add a try (i.e. correct solution does not add a tries)
            pass

        if 'submit-final-answer' == request.POST['action']:
            pass

    # --- Get Game State --- #
    # Get team
    context['team'] = get_team(context['character'])

    # Get score
    context['total_points'], context['points_reason'] = calculate_team_score(context['team'])

    # Get solved clues
    context['solved_clues'] = get_solved_clues(context['team'])

    # Get next clue
    next_clue = get_next_clue(context['team'])
    context['next_clue'] = team_to_clue_to_clue_context(next_clue) if next_clue is not None else None

    # Hint point deduction
    context['hint_cost'] = HINT_DEDUCTION

    return render(request, 'pages/home.html', context)
