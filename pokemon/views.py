
from django.http import Http404
from django.views.generic import DetailView

from .models import Pokemon


class PokemonDetail(DetailView):
    model = Pokemon

    def get_object(self):
        queryset = self.get_queryset()
        try:
            return queryset.get_by_id(self.kwargs.get(self.pk_url_kwarg))
        except self.model.DoesNotExist:
            raise Http404("Not found")
