from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required

from admin_pages.scripts.start_game import start_game
from admin_pages.scripts.make_teams import make_teams
from admin_pages.tests.helpers import make_n_users_and_characters, save_all

from characters.models import Character
from teams.models import Team

def action(request):
    '''Helper function for handling the "action" POST request'''
    context = {}

    if 'action' in request.POST.keys():
        # Console actions
        if 'start-game' == request.POST['action']:
            context['action'] = start_game()

        # Test console actions
        if 'add-default-character' == request.POST['action']:
            user, char = make_n_users_and_characters(1)
            save_all(user)
            save_all(char)
            context['action'] = 'Added 1 user'

        if 'clear-characters' == request.POST['action']:
            teams = Character.objects.all()
            num_teams = len(teams)
            for char in teams:
                user = User.objects.get(username=char.username)
                user.delete()
            context['action'] = f'Removed {num_teams - len(Character.objects.all())} Users and Characters'

        if 'clear-teams' == request.POST['action']:
            teams = Team.objects.all()
            num_teams = len(teams)
            teams.delete()
            context['action'] = f'Removed {num_teams - len(Team.objects.all())} Teams'

    return context

# Create your views here.
@staff_member_required
def console(request):
    context = action(request)
    context['reverse'] = 'admin-pages:console'

    return render(request, 'admin_pages/console.html', context)

@staff_member_required
def test_console(request):
    context = action(request)
    context['reverse'] = 'admin-pages:test-console'

    return render(request, 'admin_pages/test-console.html', context)
