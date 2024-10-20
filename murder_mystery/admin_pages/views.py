from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from admin_pages.scripts.start_game import start_game
from admin_pages.scripts.make_teams import make_teams
from admin_pages.tests.helpers import make_n_users_and_characters, save_all


# Create your views here.
@staff_member_required
def console(request):
    context = {}

    if 'action' in request.POST.keys():
        if 'start-game' == request.POST['action']:
            context['action'] = 'Game has been started'
            context['action'] = start_game()

    return render(request, 'admin_pages/console.html', context)

@staff_member_required
def test_console(request):
    context = {}

    if 'action' in request.POST.keys():
        if 'start-game' == request.POST['action']:
            context['action'] = 'Game has been started'
            context['action'] = start_game()

        if 'add-default-character' == request.POST['action']:
            user, char = make_n_users_and_characters(1)
            save_all(user)
            save_all(char)
            context['action'] = 'Added 1 user'

    return render(request, 'admin_pages/test-console.html', context)
