from django.shortcuts import render

# Create your views here.
def piPage(request):
    return render(request, 'pi.html')