import platform
from django.views import generic
# from django.urls import reverse_lazy
from django.shortcuts import redirect
# from django.shortcuts import render
# from django.views.generic import View
from .models import Room, Switch

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RoomSerializer, SwitchSerializer

if platform.platform().startswith('Linux') and platform.uname()[1] == 'raspberrypi':
    from .GPIOSwitch import setup, GPIOSwitch
else:
    from .GPIOSwitchStub import setup, GPIOSwitch


@api_view(['GET'])
def room_list(request):
    if request.method == 'GET':
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
    '''
    elif request.method == 'POST':
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    '''


@api_view(['GET', 'POST'])
def switch_list(request):
    if request.method == 'GET':
        if request.data and request.data["room_id"]:
            room_id = int(request.data["room_id"])
            switches = Room.objects.get(pk=room_id).switch_set.all()
        else:
            switches = Switch.objects.all()
        serializer = SwitchSerializer(switches, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SwitchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def switch_status(request):
    if request.method == 'GET':
        switch = Switch.objects.get(pk=request.data["switch_id"])
        serializer = SwitchSerializer(switch)
        return Response(serializer.data)


@api_view(['POST'])
def updateSwitchStatus(request):
    if request.method == 'POST':
        switch_id = request.data["switch_id"]
        switch = Switch.objects.get(pk=switch_id)
        gpioSwitch = GPIOSwitch(switch.gpio_pin)
        if gpioSwitch.getState():
            gpioSwitch.off()
            switch.status = False
        else:
            gpioSwitch.on()
            switch.status = True
        switch.save()
        return Response(SwitchSerializer(switch).data)


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
            # print("Light is on")
            gpioSwitch.on()
        else:
            # print("Light is off")
            gpioSwitch.off()


def setAllSwitchStatus():
    for switch in Switch.objects.all():
        gpioSwitch = GPIOSwitch(switch.gpio_pin)
        if gpioSwitch.getState():
            switch.status = True
        else:
            switch.status = False
        switch.save()


class SwitchView(generic.ListView):
    template_name = 'lightControl/switches.html'
    context_object_name = 'all_switches'

    def get_queryset(self):
        return Switch.objects.all()


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
        return Room.objects.all()


class DetailView(generic.DetailView):
    model = Room
    template_name = 'lightControl/detail.html'

    def get_queryset(self):
        return Room.objects.all()
