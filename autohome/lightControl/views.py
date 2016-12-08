from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Room, Switch
from GPIOSwitch import setup, GPIOSwitch


def changeSwitchStatus(request, switch_id):
    switch = Switch.objects.get(pk=switch_id)
    room = switch.room
    gpioSwitch = GPIOSwitch(switch.gpio_pin)
    
    if gpioSwitch.getState():
	gpioSwitch.off()
	switch.status = False
    else:
	gpioSwitch.on()
	switch.status = True
    switch.save()

    return redirect('lightControl:detail', pk=room.id)


def setAllSwitchesFromDB():
    setup()
    for switch in Switch.objects.all():
        gpioSwitch = GPIOSwitch(switch.gpio_pin)
        if switch.status:
            #print("Light is on")
            gpioSwitch.on()
        else:
            #print("Light is off")
            gpioSwitch.off()


def setAllSwitchStatus():
    for switch in Switch.objects.all():
        if gpioSwitch.getState():
            switch.status = True
        else:
            switch.status = False
        switch.save()


class SwitchView(generic.ListView):
    template_name = 'lightControl/switches.html'
    context_object_name = 'all_switches'


    def get_queryset(self):
        return  Switch.objects.all()


class IndexView(generic.ListView):
    template_name = 'lightControl/index.html'
    context_object_name = 'all_rooms'


    def get_queryset(self):
        '''mode = ""
        with open('/home/pi/GPIOMode.dat') as f:
            mode = f.read()
        print("The status in file is:")
        print(mode)
        if mode == "reset":
            setup()
	    with open('/home/pi/GPIOMode.dat', 'w') as f:
                f.write('set')
        '''
        return  Room.objects.all()


class DetailView(generic.DetailView):
    model = Room
    template_name = 'lightControl/detail.html'

    def get_queryset(self):
        return  Room.objects.all()




