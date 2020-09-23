from django.urls import path
from . import views

from . import views

urlpatterns = [
    path("wiki/", views.index, name="index"),
    path("wiki/<str:title>", views.displayEntry, name="displayEntry")
]
