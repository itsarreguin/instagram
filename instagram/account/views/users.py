# Django HTTP package
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# Django shortcuts
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='account:login')
def feed(request) -> HttpResponse:
    return render(request, 'users/feed.html')