from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from admin_pages.scripts.start_game import start_game
from admin_pages.scripts.make_teams import make_teams


# Create your views here.
@staff_member_required
def console(request):
    context = {}

    if 'action' in request.GET.keys():
        if 'start-game' == request.GET['action']:
            context['action'] = 'Game has been started'
            context['action'] = start_game()

        if 'team-creation' == request.GET['action']:
            # TODO: make f-string include number of teams created and what
            # teams are. Include solo team statistics
            context['action'] = 'Teams were created'
            context['action'] = make_teams()


    return render(request, 'admin_pages/console.html', context)
