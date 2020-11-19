from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Song(models.Model):
    artist = models.CharField(max_length=200)
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('myplaylist', kwargs={'id': self.id})
    

#adding a redirect url for a successful playlist creation
class Playlist(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    # Many to Many relation songs to playlist
    songs = models.ManyToManyField(Song)