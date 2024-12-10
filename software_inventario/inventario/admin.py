from django.contrib import admin
from .models import *

admin.site.register(Clientes)
admin.site.register(Categorias)
admin.site.register(Proveedores)
admin.site.register(Productos)
admin.site.register(Entradas)
admin.site.register(Salidas)
admin.site.register(StockInventarios)
admin.site.register(Usuarios)

# Register your models here.
