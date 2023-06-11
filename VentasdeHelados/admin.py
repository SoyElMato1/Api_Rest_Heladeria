from django.contrib import admin
from .models import Sabor, Tamano, Estado_Producto, Cargo, Proveedor

# Register your models here.

admin.site.register(Sabor)
admin.site.register(Tamano)
admin.site.register(Estado_Producto)
admin.site.register(Cargo)
admin.site.register(Proveedor)
