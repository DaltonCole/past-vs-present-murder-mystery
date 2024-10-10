from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import CharacterForm
from .models import Character


@login_required(login_url='accounts/signup')
def creation(request):
    context = {}

    # If this user already has a character, go back to home
    if len(Character.objects.filter(username=request.user.id)) != 0:
        return redirect('home')

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
        return redirect('home')

    context['form'] = form

    return render(request, 'characters/character_creation.html', context)
