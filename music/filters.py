import django_filters
from django_select2.forms import ModelSelect2MultipleWidget

from music.models import Musique, Style, Label, Artiste


class MusiqueFilter(django_filters.FilterSet):
    has_link = django_filters.BooleanFilter(
        label='Possède des liens',
        method='search_has_link'
    )

    class Meta:
        model = Musique
        fields = {
            'titre': ['icontains'], 'artiste': ['exact'], 'styles': ['exact']
        }

    def search_has_link(self, queryset, name, value):
        return queryset.filter(liens__isnull=not value)


class StyleFilter(django_filters.FilterSet):
    nom = django_filters.CharFilter(lookup_expr='icontains', label='Nom')

    class Meta:
        model = Style
        fields = ('nom',)


class LabelFilter(django_filters.FilterSet):
    nom = django_filters.CharFilter(lookup_expr='icontains', label='Nom')
    artistes = django_filters.ModelMultipleChoiceFilter(
        queryset=Artiste.objects.all(),
        widget=ModelSelect2MultipleWidget(
            queryset=Artiste.objects.all(),
            search_fields=['nom_artiste__icontains', 'nom__icontains', 'prenom__icontains'],
            attrs={'class': 'form-control', 'style': 'width: 100%', 'data-minimum-input-length': 0}
        )
    )
    styles = django_filters.ModelMultipleChoiceFilter(
        queryset=Style.objects.all(),
        widget=ModelSelect2MultipleWidget(
            queryset=Style.objects.all(),
            search_fields=['nom__icontains'],
            attrs={'class': 'form-control', 'style': 'width: 100%', 'data-minimum-input-length': 0}
        )
    )

    class Meta:
        model = Label
        fields = ('nom', 'artistes', 'styles')

