from django.shortcuts import render
from django.http import HttpResponse

def login_view(request):
    return render(request, 'accounts/login.html')

