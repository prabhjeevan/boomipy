from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login as dj_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Playlist, Song
from .forms import SongForm
from django.conf import settings
import billboard
import requests

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      dj_login(request, user)
      return redirect('/landing')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

@login_required
def myplaylist(request):
  # playlist = Playlist.objects.filter(user=request.user)
  playlist = Playlist.objects.all()
  username = request.user
  return render(request, 'myplaylist.html', {'playlist': playlist, 'username': username})

@login_required
def details(request, playlist_id):
  playlist = Playlist.objects.get(id=playlist_id)
  songs = Song.objects.all()
  return render(request, 'details.html', {'playlist': playlist, "id": playlist_id, 'songs': songs})

def youtube_video(request, playlist_id, song_id):
  search_url = "https://www.googleapis.com/youtube/v3/search"
  song = Song.objects.get(id=song_id)
  params = {
    'part': 'snippet',
    'q': f'{song.name} {song.artist}',
    'key': settings.YOUTUBE_DATA_API_KEY
  }

  r = requests.get(search_url, params=params)
  videoid = r.json()['items'][0]['id']['videoId']

  # vid_id = r.items[0].id.videoId
  return redirect(f'https://www.youtube.com/watch?v={videoid}')

# CRUD for playlist
class PlaylistCreate(LoginRequiredMixin, CreateView):
  model = Playlist
  fields = ['name', 'description']
  success_url = '/myplaylist/'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class PlaylistUpdate(LoginRequiredMixin, UpdateView):
  model = Playlist
  fields = ['name', 'description']
  success_url = '/myplaylist/'

class PlaylistDelete(LoginRequiredMixin, DeleteView):
  model = Playlist
  success_url = '/myplaylist/'

@login_required
def landing(request):
  username = request.user
  songchart = billboard.ChartData('hot-100')
  songs = songchart.entries
  return render(request, 'landing.html', {'name': username, 'songchart': songchart, 'songs': songs})

def login(request):
  return render(request, 'home.html')

# add an item(song) to the database
class SongCreate(LoginRequiredMixin, CreateView):
  model = Song
  fields = '__all__'
  success_url = '/myplaylist/'

# associate the song to a specific playlist
@login_required
def SongAssociate(request, playlist_id, song_id):
  Playlist.objects.get(id=playlist_id).songs.add(song_id)
  return redirect(f'/myplaylist/{playlist_id}')

# unassociate the song to a specific playlist
@login_required 
def SongUnAssociate(request, playlist_id, song_id):
  Playlist.objects.get(id=playlist_id).songs.remove(song_id)
  return redirect(f'/myplaylist/{playlist_id}')

@login_required
def AvailableSongs(request, playlist_id):
  playlist = Playlist.objects.get(id=playlist_id)
  songs = Song.objects.all()
  return render(request, 'available_songs.html', {'playlist': playlist, "id": playlist_id, 'songs': songs})

@login_required
def AddSongs(request):
  # this function will take the song names and artist names from top 100
  username = request.user
  songchart = billboard.ChartData('hot-100')
  songs = songchart.entries
  songchart2 = billboard.ChartData('billboard-200')
  songs2 = songchart2.entries

  for song in songs:
    namebillboard = song.title
    artistbillboard = song.artist
    s = Song(name = namebillboard, artist = artistbillboard)
    s.save()
  
  for song in songs:
    namebillboard2 = song.title
    artistbillboard2 = song.artist
    s = Song(name = namebillboard2, artist = artistbillboard2)
    s.save()

  return render(request, 'available_songs.html', {'name': username, 'songchart': songchart, 'songs': songs, 'songchart2': songchart2, 'songs2': songs2})
