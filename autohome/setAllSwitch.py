#!/usr/bin/env python

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autohome.settings")
django.setup()

#from lightControl import models

from lightControl.views import setAllSwitchesFromDB
#print models.Switch.objects.get(pk=1)

setAllSwitchesFromDB()

