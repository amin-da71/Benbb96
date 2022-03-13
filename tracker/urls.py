from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'tracker'

urlpatterns = [
    path('', views.tracker_list, name='liste-tracker'),
    path('<int:id>', views.tracker_detail, name='detail-tracker'),
    path('<int:pk>/update', views.TrackerUpdateView.as_view(), name='update-tracker'),
    path('<int:pk>/delete', views.TrackerDeleteView.as_view(), name='delete-tracker'),
    path('get/data/', views.tracker_data, name='tracker-data'),
    path('track/<int:pk>/update/', views.TrackUpdateView.as_view(), name='update-track'),
    path('track/<int:pk>/delete/', views.TrackDeleteView.as_view(), name='delete-track')
]
