from django.http import HttpResponse
from django.urls import path


def foundation(request):
    return HttpResponse("Application foundation")


urlpatterns = [
    path("", foundation, name="foundation"),
]
