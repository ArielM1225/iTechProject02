from django.contrib import admin
from django.http import HttpRequest
from aplicaciones.Movimientos.models import Entrada, Salida, SalidaProducto, EntradaProducto, AjusteProducto,AjusteStock, HistorialMovimiento,HistorialProductos
from aplicaciones.Productos.models import Producto

class EntradaProductoInline(admin.TabularInline):
    model = EntradaProducto
    extra = 1
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si el objeto ya existe (es una instancia guardada)
            return ['producto', 'cantidad', 'fecha_Caducidad']
        return []
    def has_delete_permission(self, request, obj=None):
        # Desactivar la opción de eliminar
        return False
    

class SalidaProductoInline(admin.TabularInline):
    model = SalidaProducto
    extra = 0
    can_delete = False
    # Sobrescribir get_readonly_fields
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si el objeto ya existe (es una instancia guardada)
            return ['producto', 'cantidad']
        return []
    def has_delete_permission(self, request, obj=None):
        # Desactivar la opción de eliminar
        return False
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "producto":
            if request.user.trabajo == 'doctor':
                # Excluir medicamentos de tipo "bajo receta duplicada"
                kwargs["queryset"] = Producto.objects.exclude(tipo_Producto='bajo receta duplicada')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    
class EntradaAdmin (admin.ModelAdmin):
    inlines = [EntradaProductoInline,]
    list_display=(
        'id_Proveedor',
        'id_Entrada',
        'created_at',
        )
    list_filter = ('id_Proveedor', 'created_at')
    
    def has_delete_permission(self, request, obj=None):
        # Desactivar la opción de eliminar
        return False
    def get_readonly_fields(self, request, obj=None):
        # Si el objeto ya existe (es una edición), solo permitimos editar el campo 'entregado'
        if obj:
            return ['id_Proveedor']  # Otros campos como solo lectura
        else:
            return []
   
    
class SalidaAdmin(admin.ModelAdmin):
    inlines = [SalidaProductoInline]  # Usamos el inline para mostrar los productos en la Salida
    list_display = ('id_Paciente', 'id_Salida', 'created_at', 'entregado',)
    list_filter = ('entregado', 'created_at')

    def get_readonly_fields(self, request, obj=None):
        # Si el objeto ya existe (es una edición), solo permitimos editar el campo 'entregado'
        if obj:
            return ['id_Paciente', 'id_Salida', 'productos', 'created_at', 'recetas', 'duplicado']  # Otros campos como solo lectura
        else:
            return []

    def has_delete_permission(self, request, obj=None):
        # Desactivar la opción de eliminar
        return False
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Si el usuario es un doctor, excluye los medicamentos bajo receta duplicada
        if request.user.trabajo == 'doctor':
            return qs.exclude(productos__tipo_Producto='bajo receta duplicada')
        
        return qs
    
   
    
    
    
    
class AjusteProductoInline(admin.TabularInline):
    model = AjusteProducto
    extra = 1  # Número de formularios adicionales vacíos
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si el objeto ya existe (es una instancia guardada)
            return ['producto', 'cantidad', 'tipo_mov']
        return []
    def has_delete_permission(self, request, obj=None):
        # Desactivar la opción de eliminar
        return False
    

# Configuración del admin para AjusteStock
class AjusteStockAdmin(admin.ModelAdmin):
    inlines = [AjusteProductoInline,]  # Inline para gestionar los productos dentro del ajuste
    list_display = (
        'id_ajuste',
        'motivo',
        'created_at'
    )
    search_fields = ['id_ajuste', 'motivo']  # Campos para búsqueda
    list_filter = ['created_at']  # Filtro por fecha de creación
    def has_delete_permission(self, request, obj=None):
        # Desactivar la opción de eliminar
        return False
    
    
class HistorialProductosInline(admin.TabularInline):
    model = HistorialProductos
    extra = 1  # Número de formularios adicionales vacíos
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si el objeto ya existe (es una instancia guardada)
            return ['producto', 'cantidad']
        return []
    def has_delete_permission(self, request, obj=None):
        # Desactivar la opción de eliminar
        return False
    
class HistorialMovimientoAdmin(admin.ModelAdmin):
    inlines = [HistorialProductosInline]
    list_display = ('tipo_movimiento','fecha_movimiento', 'motivo')
    list_filter = ('tipo_movimiento', 'fecha_movimiento')
    search_fields = ('producto__nombre_Comercial', 'motivo')
    date_hierarchy = 'fecha_movimiento'
    
    def has_delete_permission(self, request, obj=None):
        # Desactivar la opción de eliminar
        return False
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def get_readonly_fields(self, request, obj=None):
        # Campos que serán de solo lectura si el objeto ya existe
        if obj:
            readonly_fields = ['tipo_movimiento', 'fecha_movimiento', 'motivo']
            # Agregar entrada, salida y ajuste si no son None
            if obj.entrada is not None:
                readonly_fields.append('entrada')
            if obj.salida is not None:
                readonly_fields.append('salida')
            if obj.ajuste is not None:
                readonly_fields.append('ajuste')
            return readonly_fields
        return []
    
    def get_exclude(self, request, obj=None):
        """
        Excluye los campos solo si son null
        """
        if obj:  # Si el objeto existe
            exclude_fields = []
            if obj.entrada is None:
                exclude_fields.append('entrada')
            if obj.salida is None:
                exclude_fields.append('salida')
            if obj.ajuste is None:
                exclude_fields.append('ajuste')
            return exclude_fields
        return []
    
    
    
   # def save_model(self, request, obj, form, change):
        #super().save_model(request, obj, form, change)
        #for salida_producto in obj.salidaproducto_set.all():
       #     producto = salida_producto.producto
      #      producto.stock -= salida_producto.cantidad
     #       producto.save()

    #def delete_model(self, request, obj):
        # Evitar la modificación del stock al eliminar una salida
        #obj.delete()
   
#     def export_selected_to_pdf(modeladmin, request, queryset):
     
#          response = HttpResponse(content_type='application/pdf')
#          response['Content-Disposition'] = 'attachment; filename="Movimientos.pdf"'

#          p = canvas.Canvas(response, pagesize=(595, 842))  # Tamaño A4

#          pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))
#          pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
         
#          p.setFont("Arial-Bold", 12)
#          p.drawString(100, 750, "Listas de movimientos")
#          p.setFont("Arial", 12)
#          y = 720
#          for item in queryset:
#             p.drawString(120, y, f"Movimiento: {item.id_Movimiento}")
#             p.drawString(120, y - 20, f"Tipo: {item.tipo}")
#             p.drawString(120, y - 40, f"Producto: {item.id_producto}")
#             p.drawString(120, y - 80, f"Paciente: {item.id_Paciente}")
#             y -= 120
#          p.showPage()
#          p.save()
#          return response

#     export_selected_to_pdf.short_description = "Exportar Movimientos seleccionados a PDF"
#     actions = [export_selected_to_pdf]
# admin.site.register(Movimiento,MovimientoAdmin)
admin.site.register(Entrada,EntradaAdmin)
admin.site.register(Salida,SalidaAdmin)
admin.site.register(AjusteStock, AjusteStockAdmin)
admin.site.register(HistorialMovimiento, HistorialMovimientoAdmin)
