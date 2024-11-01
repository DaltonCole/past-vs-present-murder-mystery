from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, reverse

from admin_pages.scripts.start_game import start_game
from teams.models import Team

from .forms import CharacterForm
from .models import Character


@login_required(login_url='/accounts/signup')
def creation(request):
    context = {}

    # If this user already has a character, go back to home
    if len(Character.objects.filter(username=request.user.id)) != 0:
        return redirect('pages:home')

    # Create a form
    form = CharacterForm(
        request.user.id,
        request.POST or None,
        request.FILES or None,
    )

    # Save form if put request
    if form.is_valid():
        character = form.save(commit=False)
        character.username = User.objects.get(id=request.user.id)
        character.save()
        # If game has already started, give this character a team + clues
        # TODO: Add unittest for this
        if len(Team.objects.all()) > 0:
            start_game()
        return redirect('pages:home')

    context['form'] = form

    return render(request, 'characters/character_creation.html', context)
