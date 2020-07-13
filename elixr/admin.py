from django.contrib import admin
from .models import Suit,Ship,OrderedShip,OrderedSuit,Order
from django.contrib.auth.models import Group
admin.site.register(Order)
admin.site.register(OrderedSuit)
admin.site.register(OrderedShip)
admin.site.unregister(Group)
admin.site.site_header = "ELIXR."
admin.site.register(Suit)
admin.site.register(Ship)