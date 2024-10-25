from django.contrib import admin
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from aplicaciones.Productos.models import Producto, Droga, DrogaProducto, AccionFarma
from django.utils.html import format_html


    
class DrogaProductoInline(admin.TabularInline):
    model = DrogaProducto
    extra = 1  # Número de formularios adicionales que se mostrarán

class ProductosAdmin (admin.ModelAdmin):
    inlines = [DrogaProductoInline]
    exclude = ('stock', '')
    list_display=(
        'nombre_Comercial',
        'tipo_Producto',
        'stock',
        'id_Laboratorio'
    )
    
    list_filter=(
        'nombre_Comercial',
        'principio_activo',
        'tipo_Producto'
        
    ) 

class DrogaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    
class AccionFarmaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    
    # def mostrar_stock(self, obj):
    #     return calcular_stock(obj.id_producto) 

    # mostrar_stock.short_description = 'Stock Actual'
    
    

     

admin.site.register(Producto,ProductosAdmin)
admin.site.register(Droga,DrogaAdmin)
admin.site.register(AccionFarma, AccionFarmaAdmin)

