from django.contrib import admin
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
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
            # Verifica si el usuario no es superusuario
            if not request.user.is_superuser and not request.user.trabajo.producto_Psiquiatrico:
                kwargs["queryset"] = Producto.objects.exclude(tipo_Producto='bajo receta duplicada')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class EntradaProductoResource(resources.ModelResource):
    class Meta:
        model = EntradaProducto
        import_id_fields = ('id',)  # Usa un campo único para importar
        fields = ('id', 'producto', 'cantidad', 'fecha_Caducidad', 'entrada')  # Campos que queremos exportar
        export_order = ('id', 'producto', 'cantidad', 'fecha_Caducidad', 'entrada')  # Orden en que se exportarán los campos

    # Podemos realizar algunas validaciones o formateos adicionales si es necesario
    def before_import_row(self, row, **kwargs):
        # Aquí podrías agregar la lógica de validación, pero es opcional
        return row

# Recurso para SalidaProducto (los productos relacionados con Salida)
class SalidaProductoResource(resources.ModelResource):
    class Meta:
        model = SalidaProducto
        import_id_fields = ('id',)  # Usa un campo único para importar
        fields = ('id', 'producto', 'cantidad', 'salida')  # Campos que queremos exportar
        export_order = ('id', 'producto', 'cantidad', 'salida')  # Orden en que se exportarán los campos

    # Similar a EntradaProducto, puedes agregar alguna lógica adicional si lo deseas
    def before_import_row(self, row, **kwargs):
        return row

# Recurso para Entrada (con productos relacionados)
class EntradaResource(resources.ModelResource):
    productos_detalle = Field()
    proveedor_nombre = Field(attribute='id_Proveedor', column_name='Proveedor')

    class Meta:
        model = Entrada
        import_id_fields = ('id_Entrada',)
        fields = ('id_Entrada', 'proveedor_nombre', 'created_at', 'productos_detalle')
        export_order = ('id_Entrada', 'proveedor_nombre', 'created_at', 'productos_detalle')

    def dehydrate_productos_detalle(self, obj):
        productos = EntradaProducto.objects.filter(entrada=obj)
        detalles = []
        for producto in productos:
            detalles.append(f"{producto.producto.nombre_Comercial} (Cantidad: {producto.cantidad})")
        return ", ".join(detalles)

    def before_import_row(self, row, **kwargs):
        return row

class SalidaResource(resources.ModelResource):
    productos_detalle = Field()
    paciente_nombre = Field(attribute='id_Paciente', column_name='Paciente')

    class Meta:
        model = Salida
        import_id_fields = ('id_Salida',)
        fields = ('id_Salida', 'paciente_nombre', 'created_at', 'entregado', 'productos_detalle')
        export_order = ('id_Salida', 'paciente_nombre', 'created_at', 'entregado', 'productos_detalle')

    def dehydrate_productos_detalle(self, obj):
        productos = SalidaProducto.objects.filter(salida=obj)
        detalles = []
        for producto in productos:
            detalles.append(f"{producto.producto.nombre_Comercial} (Cantidad: {producto.cantidad})")
        return ", ".join(detalles)

    def before_import_row(self, row, **kwargs):
        return row

# Registrar las clases de administración con import-export en el admin
class EntradaAdmin(ImportExportModelAdmin):
    resource_class = EntradaResource
    inlines = [EntradaProductoInline]
    list_display = ('id_Proveedor', 'id_Entrada', 'created_at',)
    list_filter = ('id_Proveedor', 'created_at')

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['id_Proveedor']  # Otros campos como solo lectura
        return []

class SalidaAdmin(ImportExportModelAdmin):
    resource_class = SalidaResource
    inlines = [SalidaProductoInline]
    list_display = ('id_Paciente', 'id_Salida', 'created_at', 'entregado',)
    list_filter = ('entregado', 'created_at')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['id_Paciente', 'id_Salida', 'productos', 'created_at', 'recetas', 'duplicado']  # Otros campos como solo lectura
        return []

    def has_delete_permission(self, request, obj=None):
        return False

    

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

class HistorialProductosResource(resources.ModelResource):
    class Meta:
        model = HistorialProductos
        import_id_fields = ('id',)  # ID único para importar
        fields = ('id', 'producto', 'cantidad', 'historial_movimiento')  # Campos a exportar
        export_order = ('id', 'producto', 'cantidad', 'historial_movimiento')  # Orden de las columnas

    def before_export(self, queryset, *args, **kwargs):
        return queryset

# Recurso para HistorialMovimiento (incluye productos relacionados)
class HistorialMovimientoResource(resources.ModelResource):
    # Campo calculado para exportar los detalles de los productos relacionados
    productos_detalle = Field()

    class Meta:
        model = HistorialMovimiento
        import_id_fields = ('id_historial',)  # ID único para importar
        fields = ('id_historial', 'tipo_movimiento', 'fecha_movimiento', 'motivo', 'productos_detalle')
        export_order = ('id_historial', 'tipo_movimiento', 'fecha_movimiento', 'motivo', 'productos_detalle')

    def dehydrate_productos_detalle(self, obj):
        productos = HistorialProductos.objects.filter(historial=obj)  # Corregir a "historial" si ese es el nombre correcto
        detalles = []
        for producto in productos:
            detalles.append(f"{producto.producto.nombre_Comercial} (Cantidad: {producto.cantidad})")
        return ", ".join(detalles)

    def before_export(self, queryset, *args, **kwargs):
        return queryset

# Inline para mostrar los productos relacionados en la administración
class HistorialProductosInline(admin.TabularInline):
    model = HistorialProductos
    extra = 1

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['producto', 'cantidad']  # Los productos y las cantidades son solo lectura
        return []

    def has_delete_permission(self, request, obj=None):
        return False  # No permitir eliminar productos desde el inline

# Clase de administración para HistorialMovimiento
class HistorialMovimientoAdmin(ImportExportModelAdmin):
    resource_class = HistorialMovimientoResource
    inlines = [HistorialProductosInline]  # Agregar el inline de productos
    list_display = ('tipo_movimiento', 'fecha_movimiento', 'motivo')  # Mostrar en la lista de administración
    list_filter = ('tipo_movimiento', 'fecha_movimiento')  # Filtros en el listado
    search_fields = ('producto__nombre_Comercial', 'motivo')  # Búsqueda por nombre de producto y motivo
    date_hierarchy = 'fecha_movimiento'  # Jerarquía de fechas para filtrado rápido

    def has_delete_permission(self, request, obj=None):
        return False  # No permitir eliminar registros de HistorialMovimiento

    def has_add_permission(self, request, obj=None):
        return False  # No permitir agregar nuevos registros desde la administración

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
