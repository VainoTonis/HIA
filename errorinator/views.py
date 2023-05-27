from django.shortcuts import render

def errorRedirect(request, exception):
    return render(request, 'errorinator.html', {'error_message': 'Page not found'})
