from django.contrib import admin
from django.db import models
from django.utils.html import format_html

from avis.forms import AvisForm, ProduitForm
from .models import Profil, TypeStructure, Structure, Produit, Avis, CategorieProduit


@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'nbAvis', 'note_moyenne', 'date_creation')
    search_fields = ('user__username',)
    ordering = ('user',)

    def nbAvis(self, profil):
        return profil.avis_set.count()

    nbAvis.short_description = "Nombre d'avis"


@admin.register(CategorieProduit)
class CategorieProduitAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)
    prepopulated_fields = {'slug': ('nom',), }


class ProduitInLine(admin.StackedInline):
    model = Produit
    exclude = ('photo', )
    extra = 1
    show_change_link = True

    form = ProduitForm


@admin.register(TypeStructure)
class TypeStructureAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)
    autocomplete_fields = ('categories',)


@admin.register(Structure)
class StructureAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'apercu_informations', 'adresse', 'position_map', 'telephone', 'nb_produit', 'moyenne', 'date_creation')
    search_fields = ('nom', 'adresse')
    date_hierarchy = 'date_creation'
    ordering = ('nom', 'date_creation')
    prepopulated_fields = {'slug': ('nom',), }

    inlines = [
        ProduitInLine,
    ]

    def get_queryset(self, request):
        # Ajoute la moyenne et le nombre de produit sur chacunes des structures
        qs = super(StructureAdmin, self).get_queryset(request)
        qs = qs.annotate(moyenne=models.Avg('produit__avis__note'))
        qs = qs.annotate(nb_produit=models.Count('produit'))
        return qs

    def moyenne(self, structure):
        return structure.note_moyenne
    moyenne.admin_order_field = 'moyenne'

    def nb_produit(self, structure):
        return structure.produit_set.count()
    nb_produit.admin_order_field = 'nb_produit'

    nb_produit.short_description = 'Nombre de produit'

    def position_map(self, instance):
        if instance.adresse is not None:
            # TODO Maybe need to add client ID and signature
            return format_html('<img src="http://maps.googleapis.com/maps/api/staticmap?key=AIzaSyC9uAZiNr9tAg4Y_Vc3xvlpFsCVBB2goEw&center=%(latitude)s,%(longitude)s&zoom=%(zoom)s&size=%(width)sx%(height)s&maptype=roadmap&markers=%(latitude)s,%(longitude)s&sensor=false&visual_refresh=true&scale=%(scale)s" width="%(width)s" height="%(height)s">' % {
                'latitude': instance.adresse.latitude,
                'longitude': instance.adresse.longitude,
                'zoom': 14,
                'width': 100,
                'height': 100,
                'scale': 2
            })


class AvisInLine(admin.StackedInline):
    model = Avis
    fields = ('avis', 'note', 'photo')
    extra = 1
    show_change_link = True
    ordering = ('date_creation',)

    form = AvisForm


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'structure', 'apercu_description', 'prix', 'moyenne', 'total_avis')
    list_filter = ('structure', )
    search_fields = ('nom', 'description', 'structure__nom')
    date_hierarchy = 'date_creation'
    ordering = ('-date_creation',)
    autocomplete_fields = ('structure', 'categories')
    save_on_top = True

    form = ProduitForm

    inlines = [
        AvisInLine,
    ]

    def get_queryset(self, request):
        # Ajoute la note moyenne du produit et le nombre total d'avis sur chacun des produits
        qs = super(ProduitAdmin, self).get_queryset(request)
        qs = qs.annotate(moyenne=models.Avg('avis__note'))
        qs = qs.annotate(total=models.Count('avis__note'))
        return qs

    def save_formset(self, request, form, formset, change):
        if formset.model == Avis:
            avis_set = formset.save(commit=False)
            for avis in avis_set:
                avis.auteur = request.user.profil
                avis.save()
        else:
            formset.save()

    def nbAvis(self, produit):
        return produit.avis_set.count()

    nbAvis.short_description = "Nombre d'avis"

    def moyenne(self, obj):
        return obj.moyenne

    moyenne.admin_order_field = 'moyenne'

    def total_avis(self, obj):
        return obj.total

    total_avis.admin_order_field = 'total'


@admin.register(Avis)
class AvisAdmin(admin.ModelAdmin):
    list_display = ('id', 'structure', 'produit', 'auteur', 'apercu_avis', 'note', 'date_creation', 'date_edition', 'prive')
    list_filter = ('auteur', 'note', 'prive')
    search_fields = ('produit__nom', 'produit__structure__nom', 'auteur__user__username')
    date_hierarchy = 'date_creation'
    autocomplete_fields = ('produit',)
    readonly_fields = ('date_creation', 'date_edition')

    form = AvisForm

    def structure(self, avis):
        return avis.produit.structure

    structure.short_description = "Structure"

    def get_form(self, request, obj=None, **kwargs):
        # Pré-rempli automatiquement avec l'utilisateur connecté
        form = super(AvisAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['auteur'].initial = Profil.objects.get(user=request.user)
        return form

    def thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" height="50px" />', obj.get_photo_url())
        return 'Avis n°' + obj.id
