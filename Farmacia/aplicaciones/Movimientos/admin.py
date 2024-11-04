from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.http import HttpRequest
from aplicaciones.Movimientos.models import (
    Entrada, Salida, SalidaProducto, EntradaProducto,
    AjusteProducto, AjusteStock, HistorialMovimiento, HistorialProductos
)
from aplicaciones.Productos.models import Producto

class EntradaProductoInline(admin.TabularInline):
    model = EntradaProducto
    extra = 1

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si el objeto ya existe (es una instancia guardada)
            return ['producto', 'cantidad', 'fecha_Caducidad']
        return []

    def has_delete_permission(self, request, obj=None):
        return False

class SalidaProductoInline(admin.TabularInline):
    model = SalidaProducto
    extra = 0
    can_delete = False

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si el objeto ya existe (es una instancia guardada)
            return ['producto', 'cantidad']
        return []

    def has_delete_permission(self, request, obj=None):
        return False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "producto":
            if not request.user.trabajo.producto_Psiquiatrico:
                kwargs["queryset"] = Producto.objects.exclude(tipo_Producto='bajo receta duplicada')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class EntradaAdmin(admin.ModelAdmin):
    inlines = [EntradaProductoInline]
    list_display = ('id_Proveedor', 'id_Entrada', 'created_at',)
    list_filter = ('id_Proveedor', 'created_at')

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['id_Proveedor']  # Otros campos como solo lectura
        return []

class SalidaAdmin(admin.ModelAdmin):
    inlines = [SalidaProductoInline]
    list_display = ('id_Paciente', 'id_Salida', 'created_at', 'entregado',)
    list_filter = ('entregado', 'created_at')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['id_Paciente', 'id_Salida', 'productos', 'created_at', 'recetas', 'duplicado']  # Otros campos como solo lectura
        return []

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.trabajo.producto_Psiquiatrico:
            return qs.exclude(productos__tipo_Producto='bajo receta duplicada')
        return qs

class AjusteProductoInline(admin.TabularInline):
    model = AjusteProducto
    extra = 1

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['producto', 'cantidad', 'tipo_mov']
        return []

    def has_delete_permission(self, request, obj=None):
        return False

class AjusteStockAdmin(admin.ModelAdmin):
    inlines = [AjusteProductoInline]
    list_display = ('id_ajuste', 'motivo', 'created_at')
    search_fields = ['id_ajuste', 'motivo']
    list_filter = ['created_at']

    def has_delete_permission(self, request, obj=None):
        return False

class HistorialProductosInline(admin.TabularInline):
    model = HistorialProductos
    extra = 1

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['producto', 'cantidad']
        return []

    def has_delete_permission(self, request, obj=None):
        return False

# Recurso para HistorialMovimiento
class HistorialMovimientoResource(resources.ModelResource):
    class Meta:
        model = HistorialMovimiento
        import_id_fields = ('id_historial',)  # Cambia este campo por el ID único de HistorialMovimiento

class HistorialMovimientoAdmin(ImportExportModelAdmin):
    resource_class = HistorialMovimientoResource
    inlines = [HistorialProductosInline]
    list_display = ('tipo_movimiento', 'fecha_movimiento', 'motivo')
    list_filter = ('tipo_movimiento', 'fecha_movimiento')
    search_fields = ('producto__nombre_Comercial', 'motivo')
    date_hierarchy = 'fecha_movimiento'

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            readonly_fields = ['tipo_movimiento', 'fecha_movimiento', 'motivo']
            if obj.entrada is not None:
                readonly_fields.append('entrada')
            if obj.salida is not None:
                readonly_fields.append('salida')
            if obj.ajuste is not None:
                readonly_fields.append('ajuste')
            return readonly_fields
        return []

    def get_exclude(self, request, obj=None):
        if obj:
            exclude_fields = []
            if obj.entrada is None:
                exclude_fields.append('entrada')
            if obj.salida is None:
                exclude_fields.append('salida')
            if obj.ajuste is None:
                exclude_fields.append('ajuste')
            return exclude_fields
        return []

# Registro de modelos en el admin
admin.site.register(Entrada, EntradaAdmin)
admin.site.register(Salida, SalidaAdmin)
admin.site.register(AjusteStock, AjusteStockAdmin)
admin.site.register(HistorialMovimiento, HistorialMovimientoAdmin)
