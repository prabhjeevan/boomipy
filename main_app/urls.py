from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
  path('', views.login, name='login'),
  # user log in
  path('accounts/', include('django.contrib.auth.urls')),
  path('accounts/signup', views.signup, name='signup'),
  #  landing page
  path('landing/', views.landing, name='landing'),
  # user playlists
  path('myplaylist/', views.myplaylist, name='myplaylist'),
  # CRUD for playlist
  path('myplaylist/create', views.PlaylistCreate.as_view(), name='playlist_create'),
  path('myplaylist/<int:pk>/update', views.PlaylistUpdate.as_view(), name='playlist_update'),
  path('myplaylist/<int:pk>/delete', views.PlaylistDelete.as_view(), name='playlist_delete'),
  # playlist details
  path('myplaylist/<int:playlist_id>', views.details, name='playlist_details'),
  # Song CRUD
  path('myplaylist/song/create', views.SongCreate.as_view(), name='song_create'),
  path('myplaylist/<int:playlist_id>/add/<int:song_id>', views.SongAssociate, name='song_associate'),  
  path('myplaylist/<int:playlist_id>/remove/<int:song_id>', views.SongUnAssociate, name='song_unassociate'), 
  path('myplaylist/<int:playlist_id>/<int:song_id>', views.youtube_video, name='youtube'),
  path('myplaylist/<int:playlist_id>/songs', views.AvailableSongs, name="availabe_songs"),
  path('myplaylist/add-songs', views.AddSongs, name="add_songs"),
  ]
