from django.db import models
class Location(models.Model):
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.location

class Organization(models.Model):
    organization = models.CharField(max_length=100)

    def __str__(self):
        return self.organization

class Position(models.Model):
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.position
