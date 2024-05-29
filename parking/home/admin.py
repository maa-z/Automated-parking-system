from django.contrib import admin

# Register your models here.

from .models import Cars
from .models import Parking
from .models import CustomUser
from .models import Slots
from .models import Spots

admin.site.register(Cars)
admin.site.register(Parking)
admin.site.register(CustomUser)
admin.site.register(Slots)
admin.site.register(Spots)

