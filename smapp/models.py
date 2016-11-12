from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


# Create your models here.
class Building(models.Model):
    name = models.CharField(max_length=40)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.name)


class Apartment(models.Model):
    number = models.IntegerField(unique=True)
    floor = models.IntegerField()
    building = models.ForeignKey(Building)

    def __unicode__(self):
        return unicode(self.id)


class UserSM(models.Model):
    OWNER = 'O'
    CONCIERGE = 'C'
    RESIDENT = 'R'
    USER_TYPE_CHOICES = (
        (OWNER, 'Owner'),
        (CONCIERGE, 'Concierge'),
        (RESIDENT, 'Resident'),
    )
    userOrigin = models.OneToOneField(User)
    apartment = models.ForeignKey(Apartment, blank=True, null=True)
    building = models.ForeignKey(Building, blank=True, null=True)
    rut = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    user_type = models.CharField(
        max_length=1,
        choices=USER_TYPE_CHOICES,
    )

    def __unicode__(self):
        return self.userOrigin.username


class Visit(models.Model):
    name = models.CharField(max_length=60)
    rut = models.CharField(max_length=10)
    date = models.DateTimeField(default=datetime.now)
    resident = models.ForeignKey(UserSM, limit_choices_to={'user_type': 'R'})
    note = models.TextField(max_length=200)
    received = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.id)



"""
class Owner(models.Model):
    rut = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.id)


class Concierge(models.Model):
    userOrigin = models.OneToOneField(User)
    rut = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=20)

    def __unicode__(self):
        return self.userOrigin.username


class Resident(models.Model):
    userOrigin = models.OneToOneField(User)
    rut = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=20)
    owner = models.BooleanField(default=False)
    apartment = models.ForeignKey(Apartment)

    def __unicode__(self):
        return self.userOrigin.username

"""