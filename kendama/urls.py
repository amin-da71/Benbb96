from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'kendama'

urlpatterns = [
    # Tricks
    path('tricks/', views.KendamaTrickList.as_view(), name='tricks'),
    path('tricks/<slug:slug>/', views.KendamaTrickDetail.as_view(), name='detail-trick'),
    path('tricks/create', views.KendamaTrickCreate.as_view(), name='create-trick'),
    path('tricks/<slug:slug>/update', views.KendamaTrickUpdate.as_view(), name='update-trick'),
    path('tricks/<slug:slug>/delete', views.KendamaTrickDelete.as_view(), name='delete-trick'),

    # Combos
    path('combos/', views.ComboList.as_view(), name='combos'),
    path('combos/<slug:slug>/', views.ComboDetail.as_view(), name='detail-combo'),
    path('combos/create', views.ComboCreate.as_view(), name='create-combo'),
    path('combos/<slug:slug>/update', views.ComboUpdate.as_view(), name='update-combo'),
    path('combos/<slug:slug>/delete', views.ComboDelete.as_view(), name='delete-combo'),
    path('combos/create-trick', views.create_trick_from_modal, name='create-trick-from-modal'),

    # Common
    path(
        '<str:cls>/<int:obj_id>/update-frequency',
        views.update_player_frequency,
        name='update_player_frequency'
    ),
    path(
        'frequency-history',
        views.frequency_history,
        name='frequency_history'
    ),

    # Ladders
    path('ladders/', views.LadderList.as_view(), name='ladders'),
    path('ladders/<slug:slug>/', views.LadderDetail.as_view(), name='detail-ladder'),
    path('ladders/create', views.LadderCreate.as_view(), name='create-ladder'),
    path('ladders/<slug:slug>/update', views.LadderUpdate.as_view(), name='update-ladder'),
    path('ladders/<slug:slug>/delete', views.LadderDelete.as_view(), name='delete-ladder'),

    # Kendamas
    path('', views.KendamaList.as_view(), name='kendamas'),
    path('<slug:slug>/', views.KendamaDetail.as_view(), name='detail-kendama'),
    path('create', views.KendamaCreate.as_view(), name='create-kendama'),
    path('<slug:slug>/update', views.KendamaUpdate.as_view(), name='update-kendama'),
    path('<slug:slug>/delete', views.KendamaDelete.as_view(), name='delete-kendama'),

    # Profil
    path('profil/<str:username>', views.profil_page, name='profil'),

    path('test/', TemplateView.as_view(template_name='kendama/base.html'), name='test-page'),
]
