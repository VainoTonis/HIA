from django.shortcuts import render

# Create your views here.
def landingPage(request):
    context = {
        'title': 'REEEE',
        'description': 'Megasonic'
    }
    return render(request, 'landing.html', context)