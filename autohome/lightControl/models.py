from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse

class Room(models.Model):
    rtype = models.CharField(max_length=100)
    rname = models.CharField(max_length=100)
    rown =models.CharField(max_length=100)
    room_logo = models.CharField(max_length=1000, default=None)

    def get_absolute_url(self):
        return reverse('lighControl:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.rname + " - " + self.rtype + " - " + self.rown

class Switch(models.Model): 
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    switch_name = models.CharField(max_length=20)
    status = models.BooleanField(default=False)
    gpio_pin = models.IntegerField(default=1)

    def __str__(self):
        #room = str(self.room)
        return self.room.rname + " - " + self.switch_name

