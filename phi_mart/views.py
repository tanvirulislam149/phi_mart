from django.shortcuts import redirect
from django.http import HttpResponse

def home(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return redirect('/api/v1/')