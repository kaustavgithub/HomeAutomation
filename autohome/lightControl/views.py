from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Room, Switch
from GPIOSwitch import setup, GPIOSwitch

from django.conf import settings

import time,threading


def performThread(switch_id, timerType, duration):
    TIMER_DICT = getattr(settings, "TIMER_DICT", None)
    if (switch_id, timerType) in TIMER_DICT:
        timerThread = TIMER_DICT[(switch_id, timerType)]
    else:
        timerThread = setTimer(switch_id, timerType, duration)
        TIMER_DICT[(switch_id, timerType)] = onThread

    if(timerThread.isAlive()):
        if(duration==0):
            timerThread.stop()
        else:
            timerThread.changeDuration(duration)
    else:
        timerThread.start()


def setOnTimer(switch_id, duration):
    timerType = 'ON'
    performThread(switch_id, timerType, duration)


def setOffTimer(switch_id, timerType, duration):
    timerType = 'OFF'
    performThread(switch_id, timerType, duration)


class setTimer(threading.Thread):
    def __init__(self, switch_id, timerType, duration):
        self.switch_id = switch_id
        self.timerType = timerType
        self.duration = duration * 60
        self._stop_event = threading.Event()
        self._durationCount = 0

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def changeDuration(self, duration):
        self.duration = duration

    def run(self):
        while(not self.stopped()):
            time.sleep(1)
            if (self._durationCount>=self.duration):
                switch = Switch.objects.get(pk=self.switch_id)
                room = switch.room
                gpioSwitch = GPIOSwitch(switch.gpio_pin)

                if self.timerType=='OFF':
                    gpioSwitch.off()
                    switch.status = False
                else:
                    gpioSwitch.on()
                    switch.status = True
                switch.save()
                break
            else:
                self._durationCount += 1



def setOffTimer(request, switch_id):
    switch = Switch.objects.get(pk=switch_id)
    room = switch.room
    gpioSwitch = GPIOSwitch(switch.gpio_pin)

    return redirect('lightControl:detail', pk=room.id)


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




