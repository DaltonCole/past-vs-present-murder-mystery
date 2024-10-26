from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import render

from admin_pages.scripts.make_unique_default_users_and_chars import (
    make_unique_default_users_and_chars,
)
from admin_pages.scripts.start_game import start_game
from admin_pages.tests.helpers import make_n_users_and_characters, save_all
from bonus_points.models import TeamToBonusPoint
from characters.models import Character
from teams.models import Team, TeamToClue

def action(request):
    '''Helper function for handling the "action" POST request'''
    context = {}

    if 'action' in request.POST.keys():
        # Console actions
        if 'start-game' == request.POST['action']:
            context['action'] = start_game()

        # Test console actions
        if 'add-default-characters' == request.POST['action']:
            make_unique_default_users_and_chars()
            context['action'] = 'Added 10 user'

        if 'clear-characters' == request.POST['action']:
            users = User.objects.exclude(id=request.user.id)
            count = 0
            for user in users:
                user.delete()
                count += 1
            context['action'] = f'Removed {count} Users'

        if 'clear-teams' == request.POST['action']:
            teams = Team.objects.all()
            num_teams = len(teams)
            teams.delete()
            context['action'] = f'Removed {num_teams - len(Team.objects.all())} Teams'

        if 'reset-hints' == request.POST['action']:
            for clue in TeamToClue.objects.all():
                clue.location_hints = 0
                clue.save()
            context['action'] = f'Reset location hints'

        if 'reset-finds' == request.POST['action']:
            for clue in TeamToClue.objects.all():
                clue.location_hints = 0
                clue.found = False
                clue.save()
            context['action'] = f'Reset clue finds and hints'

        if 'reset-bonus-points' == request.POST['action']:
            TeamToBonusPoint.objects.all().delete()
            context['action'] = f'Reset bonus points'

    return context

# Create your views here.
@staff_member_required
def console(request):
    context = action(request)
    context['reverse'] = 'admin-pages:console'

    return render(request, 'admin_pages/console.html', context)

# TODO: Uncomment
#@staff_member_required
def test_console(request):
    context = action(request)
    context['reverse'] = 'admin-pages:test-console'

    return render(request, 'admin_pages/test-console.html', context)
