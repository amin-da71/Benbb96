from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.html import format_html
from django.utils.timezone import make_aware, make_naive
from django.views.decorators.http import require_POST
from django.views.generic import UpdateView, DeleteView
from django_pandas.io import read_frame
import pandas as pd
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from tracker.forms import TrackForm, TrackerForm
from tracker.models import Tracker, Track
from tracker.serializers import TrackerSerializer, CustomTrackSerializer, TrackSerializer


class TrackerView(ModelViewSet):
    queryset = Tracker.objects.all()
    serializer_class = TrackerSerializer

    def get_queryset(self):
        return self.request.user.profil.trackers.all()

    def perform_create(self, serializer):
        serializer.save(createur=self.request.user)


class TrackView(ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer

    def get_queryset(self):
        return super().get_queryset().filter(tracker__createur__user=self.request.user)


@login_required
def tracker_list(request):
    trackers = Tracker.objects.filter(createur=request.user.profil)

    form = TrackerForm(request.POST or None)
    if form.is_valid():
        if trackers.filter(nom=form.cleaned_data['nom']).exists():
            form.add_error('nom', 'Vous avez déjà créé un tracker du même nom.')
        else:
            tracker = form.save(commit=False)
            tracker.createur = request.user.profil
            tracker.save()

            return redirect('tracker:liste-tracker')

    return render(request, 'tracker/tracker_list.html', {'trackers': trackers, 'form': form})


class TrackerUpdateView(UpdateView):
    model = Tracker
    form_class = TrackerForm

    def get_queryset(self):
        return self.request.user.profil.trackers.all()


class TrackerDeleteView(DeleteView):
    model = Tracker
    success_url = reverse_lazy('tracker:liste-tracker')

    def get_queryset(self):
        return self.request.user.profil.trackers.all()


@login_required
def tracker_quick_add(request, pk):
    tracker = get_object_or_404(Tracker.objects.filter(createur=request.user.profil), id=pk)
    Track.objects.create(tracker=tracker)
    messages.success(request, 'Un track a bien été ajouté sur le tracker %s' % tracker)
    return redirect('tracker:liste-tracker')


@login_required
def tracker_detail(request, pk):
    tracker = get_object_or_404(Tracker.objects.filter(createur=request.user.profil), id=pk)

    form = TrackForm(request.POST or None, initial={'datetime': timezone.now()})
    if form.is_valid():
        track = form.save(commit=False)
        track.tracker = tracker
        track.save()
        return redirect(tracker)

    tracks = tracker.tracks.all()
    for track in tracks:
        track.form = TrackForm(instance=track)

    return render(request, 'tracker/tracker_detail.html', {
        'tracker': tracker,
        'tracks': tracks,
        'form': form
    })


class TrackUpdateView(generics.UpdateAPIView):
    queryset = Track.objects.all()
    serializer_class = CustomTrackSerializer


class TrackDeleteView(generics.DestroyAPIView):
    queryset = Track.objects.all()
    serializer_class = CustomTrackSerializer


def get_tracks_from_request(request):
    tracker = get_object_or_404(Tracker.objects.filter(createur=request.user.profil), id=request.POST.get('id'))

    start = request.POST.get('start', None)
    end = request.POST.get('end', None)

    tracks = tracker.tracks.all()
    if start:
        start = make_aware(datetime.strptime(start, '%y-%m-%d %H:%M:%S'))
        tracks = tracks.filter(datetime__gte=start)
    if end:
        end = make_aware(datetime.strptime(end, '%y-%m-%d %H:%M:%S'))
        tracks = tracks.filter(datetime__lte=end)

    return tracks


@require_POST
def tracker_data(request):
    if not request.is_ajax():
        return JsonResponse({'error': 'Unauthorized access'}, status=401)

    tracks = get_tracks_from_request(request)

    labels = []
    data = []
    avg = 0

    if tracks.exists():
        # Regroupe les données par date pour faire des stats
        frequency = request.POST.get('frequency', 'D')
        df = read_frame(tracks, fieldnames=['datetime'])
        df['datetime'] = pd.to_datetime(df['datetime'])
        df['datetime'] = df['datetime'].dt.tz_convert('Europe/Paris')
        df.index = df['datetime']
        df['count'] = [1] * tracks.count()
        data = df.resample(frequency).sum()

        delta = timezone.now().date() - tracks.earliest('datetime').datetime.date()

        date_format = '%d/%m/%y'
        avg = tracks.count() / (delta.days + 1)  # On ajoute un jour pour éviter la division par 0

        if frequency == 'H':
            date_format = '%d/%m/%y %M:%H'
            avg /= 24
        elif frequency == 'W':
            avg *= 7
        elif frequency == 'M':
            date_format = '%B %Y'
            avg *= 30
        elif frequency == 'Q':
            date_format = '%B %Y'
            avg *= 120
        elif frequency == 'Y':
            date_format = '%Y'
            avg *= 365

        data.index = data.index.strftime(date_format)

        labels = data.index.values.tolist()
        data = data.values.tolist()

        # TODO Faire en sorte que tous les dates entre le dernier track et ojd apparaissent
        # Ajoute la date d'aujourd'hui si elle n'y est pas déjà
        # today = timezone.now().strftime(date_format)
        # if today not in labels:
        #     labels.append(today)
        #     data.append([0])

    return JsonResponse({
        'labels': labels,
        'data': data,
        'avg': round(avg, 2)
    })


def format_timedelta(td):
    """
    Formate correctement un écart de temps avec les jours, heures, minutes et secondes

    :param timedelta td: le timedelta à formater
    :return: la chaîne de caractère formatée
    :rtype: str
    """
    seconds = td.total_seconds()
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return '%d jour%s %dh %dm %ds' % (days, ('s' if days > 1 else ''), hours, minutes, seconds)
    elif hours > 0:
        return '%dh %dm %ds' % (hours, minutes, seconds)
    elif minutes > 0:
        return '%dm %ds' % (minutes, seconds)
    else:
        return '%ds' % seconds


def get_other_stats(request):
    if not request.is_ajax():
        return JsonResponse({'error': 'Unauthorized access'}, status=401)

    tracks = get_tracks_from_request(request)

    if not tracks.exists():
        return JsonResponse({})

    hours = {}
    for i in range(24):
        hours[str(i)] = 0

    weekdays = {
        0: 'Lundi',
        1: 'Mardi',
        2: 'Mercredi',
        3: 'Jeudi',
        4: 'Vendredi',
        5: 'Samedi',
        6: 'Dimanche'
    }
    days = {}
    for weekday in weekdays.values():
        days[weekday] = 0

    deltas = []
    prev = minimum = maximum = None
    min_1 = min_2 = max_1 = max_2 = None
    for track in tracks:
        dt = make_naive(track.datetime)
        hours[str(dt.hour)] += 1
        days[weekdays[dt.weekday()]] += 1
        if prev:
            # Store the diff between the previous track and this one
            delta = prev.datetime - track.datetime
            deltas.append(delta)
            # Keep min and max with their respective datetime
            if not minimum or delta < minimum:
                minimum = delta
                min_1 = timezone.localtime(track.datetime)
                min_2 = timezone.localtime(prev.datetime)
            if not maximum or delta > maximum:
                maximum = delta
                max_1 = timezone.localtime(track.datetime)
                max_2 = timezone.localtime(prev.datetime)

        prev = track

    delta_stats = None
    if deltas:
        date_format = '%d/%m/%y %H:%M'
        delta_stats = {
            'deltaMin': format_html(
                '<b>{}</b> <br><small>Entre le {} et le {}</small>',
                format_timedelta(minimum), min_1.strftime(date_format), min_2.strftime(date_format)
            ),
            'deltaAvg': format_timedelta(sum(deltas, timedelta(0)) / len(deltas)),
            'deltaMax': format_html(
                '<b>{}</b> <br><small>Entre le {} et le {}</small>',
                format_timedelta(maximum), max_1.strftime(date_format), max_2.strftime(date_format)
            )
        }

    return JsonResponse({
        'trackByHourChart': {
            'labels': list(x + 'h' for x in hours.keys()),
            'values': list(hours.values())
        },
        'trackByDayChart': {
            'labels': list(days.keys()),
            'values': list(days.values())
        },
        'deltaStats': delta_stats
    })


@require_POST
def tracker_history(request):
    if not request.is_ajax():
        return JsonResponse({'error': 'Unauthorized access'}, status=401)

    tracks = get_tracks_from_request(request)
    for track in tracks:
        track.form = TrackForm(instance=track)
    html = render_to_string('tracker/include/tbody_tracks.html', {'tracks': tracks}, request)
    return JsonResponse({
        'html': html,
        'trackCount': tracks.count()
    })
