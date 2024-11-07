import uuid

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import render

from admin_pages.scripts.make_unique_default_users_and_chars import (
    make_unique_default_users_and_chars,
)
from admin_pages.scripts.start_game import start_game
from admin_pages.tests.helpers import make_n_users_and_characters, save_all
from bonus_points.forms import AdminBonusPointForm
from bonus_points.models import BonusPoint, TeamToBonusPoint
from bonus_points.scripts.get_team_bonus_points import get_team_bonus_points
from characters.models import Character
from pages.scripts.calculate_team_score import calculate_team_score
from pages.scripts.team_to_clue_to_clue_context import team_to_clue_to_clue_context
from solutions.models import Solution
from story_clues.models import StoryClue
from teams.models import Team, TeamToClue
from teams.scripts.get_next_clue import get_next_clue
from teams.scripts.get_solved_clues import get_solved_clues
from teams.scripts.get_team import get_team
from teams.scripts.get_team_clues_in_order import get_team_clues_in_order

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

def stats(request):
    '''Get the stats of every player'''
    characters = {}

    for character in Character.objects.all().order_by('real_name'):
        team = get_team(character)
        clues = get_team_clues_in_order(team)
        hints = [team_to_clue_to_clue_context(clue) for clue in clues]
        total_score, score = calculate_team_score(team)
        solution = Solution.objects.filter(team=team).first()
        found_story_clues = [clue.location_clue.story_clue if clue.location_clue is not None else clue.character_clue.story_clue for clue in get_solved_clues(team)]
        characters[character] = {
                'team': team,
                'clues': zip(clues, hints),
                'score': score,
                'total_score': total_score,
                'solution': solution.solution if solution else None,
                'story': found_story_clues,
                }

    bonus_points = BonusPoint.objects.exclude(answer__startswith='uuid-')
    bonus_points_remaining = sum([point.amount for point in bonus_points])

    return {'characters': characters,
            'bonus_points': bonus_points,
            'total_bonus_points': bonus_points_remaining,
            }


def handle_admin_bonus_point_form(request, context):
    form = AdminBonusPointForm(
            request.POST or None
            )

    if form.is_valid():
        team = form.cleaned_data['team']
        amount = form.cleaned_data['amount']
        reason = form.cleaned_data['reason']
        answer = 'uuid-' + str(uuid.uuid4())

        max_points = 500
        if amount > max_points:
            context['action'] = f'Too many bonus points trying to be awarded. {amount} > {max_points}'
            return form

        bonus_point = BonusPoint(
                amount=amount,
                reason=reason,
                answer=answer,
                )
        bonus_point.save()
        team_to_bonus_point = TeamToBonusPoint(
                team=team,
                bonus_point=bonus_point,
                )
        team_to_bonus_point.save()
        context['action'] = f'Assigned {team} {amount} bonus points for: {reason}'

    return form

# Create your views here.
@staff_member_required
def console(request):
    context = action(request)
    context['reverse'] = 'admin-pages:console'

    context = {**context, **stats(request)}
    context['admin_bonus_point_form'] = handle_admin_bonus_point_form(request, context)

    return render(request, 'admin_pages/console.html', context)

# TODO: Uncomment
#@staff_member_required
def test_console(request):
    context = action(request)
    context['reverse'] = 'admin-pages:test-console'

    context = {**context, **stats(request)}
    context['admin_bonus_point_form'] = handle_admin_bonus_point_form(request, context)

    return render(request, 'admin_pages/test-console.html', context)
