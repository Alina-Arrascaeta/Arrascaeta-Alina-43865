from django.contrib import admin
from .models import Producto, Cliente, Proveedor, Empleado, Avatar


# Register your models here.
admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Proveedor)
admin.site.register(Empleado)
admin.site.register(Avatar)