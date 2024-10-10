from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from characters.models import Character

@login_required(login_url='accounts/signup')
def home(request):
    # Go to character creation screen if no character exists for this user
    try:
        matching_character = Character.objects.get(username=request.user.id)
    except:
        return redirect('characters:creation')

    context = {
        'matching_character': matching_character,
    }

    return render(request, 'home.html', context)

