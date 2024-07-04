from django.contrib import admin
from .models import User, Ride, RideEvent, Role

admin.site.register(User)
admin.site.register(Ride)
admin.site.register(RideEvent)
admin.site.register(Role)
