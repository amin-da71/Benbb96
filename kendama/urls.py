from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'kendama'

urlpatterns = [
    path('tricks/', views.KendamaTrickList.as_view(), name='tricks'),
    path('tricks/<slug:slug>/', views.KendamaTrickDetail.as_view(), name='detail-trick'),
    path('tricks/create', views.KendamaTrickCreate.as_view(), name='create-trick'),
    path('tricks/<slug:slug>/update', views.KendamaTrickUpdate.as_view(), name='update-trick'),
    path('tricks/<slug:slug>/delete', views.KendamaTrickDelete.as_view(), name='delete-trick'),
    path(
        'tricks/<int:trick_id>/update-frequency',
        views.update_trick_player_frequency,
        name='update_trick_player_frequency'
    ),
    path('combos/', views.ComboList.as_view(), name='combos'),
    path('combos/<slug:slug>/', views.ComboDetail.as_view(), name='detail-combo'),
    path('combos/create', views.ComboCreate.as_view(), name='create-combo'),
    path('combos/<slug:slug>/update', views.ComboUpdate.as_view(), name='update-combo'),
    path('combos/<slug:slug>/delete', views.ComboDelete.as_view(), name='delete-combo'),
    path(
        'combos/<int:combo_id>/update-frequency',
        views.update_combo_player_frequency,
        name='update_combo_player_frequency'
    ),
    path('combos/create-trick', views.create_trick_from_modal, name='create-trick-from-modal'),

    path('test/', TemplateView.as_view(template_name='kendama/base.html'), name='test-page'),
]