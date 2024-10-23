from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from bonus_points.forms import BonusPointForm
from characters.models import Character
from pages.forms import TextClueForm, VideoClueForm
from pages.scripts.calculate_team_score import calculate_team_score
from pages.scripts.calculate_team_score import HINT_DEDUCTION
from pages.scripts.team_to_clue_to_clue_context import team_to_clue_to_clue_context
from teams.models import Team
from teams.scripts.get_next_clue import get_next_clue
from teams.scripts.get_solved_clues import get_solved_clues
from teams.scripts.get_team import get_team

def found_clues(request):
    character = Character.objects.get(username=request.user.id)
    team = get_team(character)
    solved_clues = get_solved_clues(team)

    response = ''
    for i, clue in enumerate(solved_clues):
        if clue.video_clue is not None:
            response += f'<tr><td scope="row">{i}</td><td><a href="{clue.video_clue.video_url}" target="_blank">video</a></td></tr>'
        else:
            response += f'<tr><td scope="row">{i}</td><td>{clue.text_clue.story_clue.clue}</td></tr>'
    return HttpResponse(response)

def score(request):
    character = Character.objects.get(username=request.user.id)
    team = get_team(character)
    total_points, points_reason = calculate_team_score(team)

    response = ''
    for i, (point, reason) in enumerate(points_reason):
        response += f'<tr><td scope="row">{point}</td><td>{reason}</td></tr>'
    response += f'<tr><td scope="row"><b>Total:</b></td><td><b>{total_points}</b></td></tr>'
    return HttpResponse(response)

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

    # --- Clue Answer --- #
    if next_clue is not None:
        if next_clue.video_clue is not None:
            form = VideoClueForm(
                    request.POST or None,
                    request.FILES or None,
                    )
        else:
            form = TextClueForm(
                    request.POST or None,
                    request.FILES or None,
                    )

        if form.is_valid():
            if type(form) is VideoClueForm:
                answer = form.cleaned_data['answer']
                if next_clue.video_clue.location == answer:
                    next_clue.found = True
                    next_clue.save()
                    return redirect('pages:home')
                else:
                    context['incorrect'] = 'Incorrect Guess!'
                    next_clue.tries += 1
                    next_clue.save()
                    form.POST = None
            else:
                answer = int(form.cleaned_data['answer'])
                if next_clue.text_clue.character_id.id == answer:
                    next_clue.found = True
                    next_clue.save()
                    return redirect('pages:home')
                else:
                    context['incorrect'] = 'Incorrect Guess!'
                    next_clue.tries += 1
                    next_clue.save()
                    form.POST = None

        context['form'] = form

    else:
        # TODO - Allow the user to make a final guess
        context['final_guess'] = True

    # --- Bonus Point Submission --- #
    context['bonus_point_form'] = BonusPointForm()


    return render(request, 'pages/home.html', context)
