from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from characters.models import Character
from pages.scripts.calculate_team_score import calculate_team_score
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

    # Get team
    context['team'] = get_team(context['character'])

    # Get score
    context['total_points'], context['points_reason'] = calculate_team_score(context['team'])

    # Get solved clues
    context['solved_clues'] = get_solved_clues(context['team'])

    # Get next clue
    context['next_clue'] = get_next_clue(context['team'])

    return render(request, 'home.html', context)
