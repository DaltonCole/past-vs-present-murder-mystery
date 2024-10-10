from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from characters.models import Character

# Create your views here.
class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('accounts/signup'))
            return redirect('accounts/signup')
        return response
