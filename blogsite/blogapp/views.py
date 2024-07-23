from django.shortcuts import render,HttpResponse

# Create your views here.
def indexview(request):
    return HttpResponse('blogs app')