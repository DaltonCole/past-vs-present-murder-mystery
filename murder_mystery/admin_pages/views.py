from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.
@staff_member_required
def console(request):
    context = {}

    if 'action' in request.GET.keys():
        if 'team-creation' == request.GET['action']:
            # TODO: make f-string include number of teams created and what
            # teams are. Include solo team statistics
            context['action'] = 'Teams were created'

    return render(request, 'admin_pages/console.html', context)
