
from django.http import JsonResponse

def index(request):
    a = {"name" : "init api"}
    return JsonResponse(a)


