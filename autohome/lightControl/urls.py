from django.conf.urls import url
from . import views

app_name = 'lightControl'

urlpatterns = [
    # /lightControl/
    url(r'^$', views.IndexView.as_view(), name="index"),

    # /lightControl/<rooms_id>/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name="detail"),

    # /lightControl/switch/room_id/
    url(r'^switch/(?P<switch_id>[0-9]+)/change$', views.changeSwitchStatus, name="switch-update"),

    url(r'^switches/$', views.SwitchView.as_view(), name='switches'),

    url(r'^rest/api/rooms$', views.room_list),
    url(r'^rest/api/switches$', views.switch_list),
    url(r'^rest/api/switch_status$', views.switch_status),
    url(r'^rest/api/change$', views.updateSwitchStatus),

]
