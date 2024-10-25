from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from bonus_points.forms import BonusPointForm
from characters.models import Character
from pages.forms import CharacterClueForm, LocationClueForm
from pages.scripts.calculate_team_score import calculate_team_score
from pages.scripts.calculate_team_score import HINT_DEDUCTION
from pages.scripts.team_to_clue_to_clue_context import team_to_clue_to_clue_context
from solutions.forms import SolutionForm
from solutions.models import Solution
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
        story_clue = clue.location_clue.story_clue if clue.location_clue is not None else clue.character_clue.story_clue
        response += f'<tr><td scope="row">{i+1}</td><td>{story_clue}</td></tr>'
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
        if next_clue.location_clue is not None:
            form = LocationClueForm(
                    request.POST or None,
                    request.FILES or None,
                    )
        else:
            form = CharacterClueForm(
                    request.POST or None,
                    request.FILES or None,
                    )

        if form.is_valid():
            if type(form) is LocationClueForm:
                answer = form.cleaned_data['answer']
                if next_clue.location_clue.location.location == answer:
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
                if next_clue.character_clue.character_id.id == answer:
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

    # --- Final Solution --- #
    pre_populate_solution_form = {
            'solution': Solution.objects.get(team=context['team']).solution if len(Solution.objects.filter(team=context['team'])) > 0 else ''
            }
    solution_form = SolutionForm(
            request.POST or None,
            initial=pre_populate_solution_form,
            )

    if request.method == 'POST' and solution_form.is_valid():
        try:
            solution = Solution.objects.get(team=context['team'])
            solution.solution = solution_form.cleaned_data['solution']
        except:
            solution = solution_form.save(commit=False)
            solution.team = context['team']
        solution.save()

    context['solution'] = solution_form

    # --- Bonus Point Submission --- #
    context['bonus_point_form'] = BonusPointForm()


    return render(request, 'pages/home.html', context)
