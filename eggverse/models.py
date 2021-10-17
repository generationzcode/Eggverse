from django.db import models

# Create your models here.
class Planets(models.Model):
  planet_name = models.CharField(max_length=200)
  planet_coordinates = models.CharField(max_length=200)
  planet_chat = models.TextField()
  planet_landscape = models.TextField()
  planet_players = models.TextField()
  planet_collisions = models.TextField()
  planet_owner = models.CharField(max_length=200)
  taxation = models.CharField(max_length=150)
  description = models.TextField()

class Player(models.Model):
  username = models.CharField(max_length=200)
  email = models.CharField(max_length=500)
  inventory = models.TextField()
  space = models.CharField(max_length=200)
  quadrant = models.TextField()
  planet = models.CharField(max_length=200)
  balance = models.TextField()
  online = models.CharField(max_length=200)
  owned_planets = models.TextField()

