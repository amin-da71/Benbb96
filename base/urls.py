from django.urls import path
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from . import views

app_name = 'base'

urlpatterns = [
    path('', views.ProjetListView.as_view(), name='home'),
    path(_('about'), TemplateView.as_view(template_name='base/about.html'), name='about'),
    path(_('labyrinthe-game'), TemplateView.as_view(template_name='base/labyrinthe_game.html'), name='labyrinthe-game'),
    path('rallye-des-colocs', TemplateView.as_view(template_name='base/rallye.html'), name='rallye'),
    path('gallery', TemplateView.as_view(template_name='base/gallery.html'), name='gallery'),
    path('profil/<str:slug>', views.UserDetailView.as_view(), name='profil'),
    path('profil/<str:username>/update', views.update_profil, name='update_profil'),
    path(
        'profil/<str:slug>/avis',
        views.UserDetailView.as_view(template_name='base/profil/avis.html'),
        name='profil-avis'
    ),
    path(
        'profil/<str:slug>/music',
        views.UserDetailView.as_view(template_name='base/profil/music.html'),
        name='profil-music'
    ),
    path(
        'profil/<str:slug>/versus',
        views.UserDetailView.as_view(template_name='base/profil/versus.html'),
        name='profil-versus'
    ),
    path('change_password/', views.change_password, name='change_password'),
    path('signup/', views.signup, name='signup')
]
