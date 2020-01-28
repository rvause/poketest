from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "pokemon"

urlpatterns = [
    path('', TemplateView.as_view(template_name="pokemon/index.html"), name="index"),
    path("<int:pk>/", views.PokemonDetail.as_view(), name="detail"),
]
