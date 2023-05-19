# from django.shortcuts import redirect
# from django.urls import reverse

# class ESIAuth:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Check if the client is authenticated
#         if not request.session.get('authenticated'):
#             # Client is not authenticated, redirect to EVE Online login page
#             return redirect(reverse('esi_login'))

#         # Client is authenticated, proceed with the request
#         response = self.get_response(request)
#         return response