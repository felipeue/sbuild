from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


# Create your models here.
class Owner(models.Model):
    userOrigin = models.OneToOneField(User, related_name='owner')
    phone = models.CharField(max_length=20)

    def __unicode__(self):
        return str(self.id)


class Building(models.Model):
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    owner = models.ForeignKey(Owner, related_name='building')

    def __unicode__(self):
        return str(self.id)


class Apartment(models.Model):
    number = models.IntegerField(unique=True)
    floor = models.IntegerField()
    building = models.ForeignKey(Building, related_name='apartment')

    def __unicode__(self):
        return str(self.id)


class Resident(models.Model):
    userOrigin = models.OneToOneField(User)
    phone = models.CharField(max_length=20)
    apartment = models.ManyToManyField(Apartment)

    def __unicode__(self):
        return self.userOrigin.username


class Consierge(models.Model):
    userOrigin = models.OneToOneField(User)
    phone = models.CharField(max_length=20)
    building = models.ForeignKey(Building)

    def __unicode__(self):
        return self.userOrigin.username


class Visit(models.Model):
    name = models.CharField(max_length=60)
    rut = models.CharField(max_length=12)
    date = models.DateTimeField(default=datetime.now)
    resident = models.ForeignKey(Resident, related_name='visit')
    note = models.TextField(max_length=200)
    received = models.BooleanField(default=True)
    consierge = models.ForeignKey(Consierge)

    def __unicode__(self):
        return str(self.id)


class Publication(models.Model):
    publisher = models.ForeignKey(User, related_name='publication')
    title = models.CharField(max_length=100)
    date = models.DateField(default=datetime.now)
    hour = models.TimeField(default=datetime.now)
    message = models.TextField(max_length=1000)
    type = models.CharField(max_length=100)

    def __unicode__(self):
        return str(self.id)


class Location(models.Model):
    name = models.CharField(max_length=100)
    building = models.ForeignKey(Building, related_name='location')

    def __unicode__(self):
        return str(self.id)


class Event(models.Model):
    title = models.CharField(max_length=100)
    start = models.CharField(max_length=100)
    end = models.CharField(max_length=100)
    all_day = models.IntegerField()
    resident = models.ForeignKey(Resident, related_name='event')
    location = models.ForeignKey(Location, related_name='event')

    def __unicode__(self):
        return str(self.id)


class Rent(models.Model):
    month = models.CharField(max_length=50)
    amount = models.IntegerField()
    resident = models.ForeignKey(Resident, related_name='rent')
    date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return str(self.id)