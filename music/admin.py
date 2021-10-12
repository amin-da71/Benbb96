from django.contrib import admin

from music.models import Pays, Artiste, Style, Label, Playlist, Musique, MusiquePlaylist, Lien


@admin.register(Pays)
class PaysAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)


class MusiqueStyleInline(admin.TabularInline):
    model = Musique.styles.through
    autocomplete_fields = ('musique',)


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)
    save_on_top = True

    inlines = [MusiqueStyleInline]


class MusiquePlaylistInline(admin.TabularInline):
    model = MusiquePlaylist
    autocomplete_fields = ('musique',)


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'createur', 'nb_musique')
    search_fields = ('nom',)
    autocomplete_fields = ('styles',)
    prepopulated_fields = {'slug': ('nom',), }
    save_on_top = True

    inlines = [MusiquePlaylistInline]

    def get_form(self, request, obj=None, **kwargs):
        # Pré-rempli automatiquement avec l'utilisateur connecté
        form = super(PlaylistAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['createur'].initial = request.user
        return form

    def nb_musique(self, obj):
        return obj.musiqueplaylist_set.count()
    nb_musique.short_description = 'Nombre de musique'


class MusiqueInline(admin.TabularInline):
    model = Musique
    prepopulated_fields = {'slug': ('titre',), }
    autocomplete_fields = ('styles',)


@admin.register(Artiste)
class ArtisteAdmin(admin.ModelAdmin):
    list_display = ('nom_artiste', 'nom', 'prenom', 'ville', 'pays', 'date_creation', 'date_modification')
    list_filter = ('styles', 'labels', 'createur')
    search_fields = (
        'nom_artiste', 'prenom', 'nom', 'ville', 'pays__nom', 'labels__nom', 'styles__nom'
    )
    date_hierarchy = 'date_creation'
    ordering = ('-date_modification',)
    prepopulated_fields = {'slug': ('nom_artiste',), }
    readonly_fields = ('soundcloud_followers', )
    autocomplete_fields = ('styles',)

    inlines = [MusiqueInline]

    def get_form(self, request, obj=None, **kwargs):
        # Pré-rempli automatiquement avec l'utilisateur connecté
        form = super(ArtisteAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['createur'].initial = request.user
        return form


class LienInline(admin.TabularInline):
    model = Lien


@admin.register(Musique)
class MusiqueAdmin(admin.ModelAdmin):
    list_display = ('artiste', 'titre', 'album', 'createur', 'date_creation', 'date_modification')
    list_display_links = ('titre',)
    list_filter = ('styles', 'createur')
    search_fields = (
        'titre', 'artiste__nom_artiste', 'album', 'styles__nom', 'musiqueplaylist__playlist__nom'
    )
    date_hierarchy = 'date_creation'
    prepopulated_fields = {'slug': ('titre',), }
    autocomplete_fields = ('artiste', 'styles')

    inlines = [LienInline]

    def get_form(self, request, obj=None, **kwargs):
        # Pré-rempli automatiquement avec l'utilisateur connecté
        form = super(MusiqueAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['createur'].initial = request.user
        return form


@admin.register(Lien)
class LienAdmin(admin.ModelAdmin):
    list_display = ('id', 'musique', 'url', 'plateforme', 'createur', 'click_count', 'date_creation')
    list_filter = ('plateforme', 'createur')
    search_fields = (
        'musique__titre', 'musique__artiste__nom_artiste', 'plateforme'
    )
    date_hierarchy = 'date_creation'
    autocomplete_fields = ('musique',)

    def get_form(self, request, obj=None, **kwargs):
        # Pré-rempli automatiquement avec l'utilisateur connecté
        form = super(LienAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['createur'].initial = request.user
        return form


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')
    search_fields = ('nom', 'artistes__nom_artiste', 'styles__nom')
    prepopulated_fields = {'slug': ('nom',), }
    autocomplete_fields = ('artistes', 'styles')
