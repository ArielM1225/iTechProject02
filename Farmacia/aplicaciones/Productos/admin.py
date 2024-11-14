from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin
from aplicaciones.Productos.models import Producto, Droga, DrogaProducto, AccionFarma

class DrogaProductoInline(admin.TabularInline):
    model = DrogaProducto
    extra = 1  # Número de formularios adicionales que se mostrarán

class ProductoResource(resources.ModelResource):
    class Meta:
        model = Producto

class ProductosAdmin(ExportMixin, admin.ModelAdmin):  # Cambiamos a ExportMixin
    resource_class = ProductoResource  # Añadimos la clase de recursos
    inlines = [DrogaProductoInline]
    exclude = ('stock',)
    list_display = (
        'nombre_Comercial',
        'tipo_Producto',
        'stock',
        'id_Laboratorio'
    )
    
    list_filter = (
        'nombre_Comercial',
        'principio_activo',
        'tipo_Producto',
        'id_Laboratorio'
    ) 

class DrogaAdmin(ExportMixin, admin.ModelAdmin):  # Cambiamos a ExportMixin
    list_display = ('nombre',)
    search_fields = ('nombre',)
    
class AccionFarmaAdmin(ExportMixin, admin.ModelAdmin):  # Cambiamos a Exportmixin
    list_display = ('nombre',)
    search_fields = ('nombre',)

admin.site.register(Producto, ProductosAdmin)
admin.site.register(Droga, DrogaAdmin)
admin.site.register(AccionFarma, AccionFarmaAdmin)
