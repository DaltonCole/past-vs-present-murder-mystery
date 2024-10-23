from django.http import HttpResponse
from django.shortcuts import render

from bonus_points.forms import BonusPointForm
from bonus_points.models import BonusPoint, TeamToBonusPoint
from characters.models import Character
from teams.scripts.get_team import get_team

# Create your views here.
def bonus_point_submission(request):
    if request.POST:
        form = BonusPointForm(request.POST)

        if form.is_valid():
            matching_bonus_points = BonusPoint.objects.filter(answer=form.cleaned_data['answer'].lower())

            if len(matching_bonus_points) != 0:
                matching_bonus_points = matching_bonus_points[0]
                print(len(TeamToBonusPoint.objects.filter(bonus_point=matching_bonus_points)))

                if len(TeamToBonusPoint.objects.filter(bonus_point=matching_bonus_points)) != 0:
                    return HttpResponse('Bonus Points Already Claimed By Someone!')
                else:
                    char = Character.objects.get(username=request.user.id)
                    team = get_team(char)
                    team_to_bonus = TeamToBonusPoint(team=team, bonus_point=matching_bonus_points)
                    team_to_bonus.save()
                    return HttpResponse(f'You\'ve been awareded {matching_bonus_points.amount} bonus point(s)!')


    return HttpResponse('WRONG!')
