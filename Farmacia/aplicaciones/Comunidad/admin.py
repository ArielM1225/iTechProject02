from django.contrib import admin
from django.utils.html import format_html
from io import BytesIO
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.http import HttpResponse
from datetime import date
from aplicaciones.Comunidad.models import Empleado,Proveedor,Paciente,contacto,Laboratorio, provincia, localidad, Puesto




class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'dni', 'first_name', 'last_name', 'trabajo',  'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'email', 'dni', 'trabajo')}),
        ('Contacto', {'fields': ('id_Contacto',)}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    def get_queryset(self, request):
        # Si el usuario es superuser, puede ver a todos
        qs = super(EmpleadoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Si no es superuser, solo verá su propio registro
        return qs.filter(id=request.user.id)
    
    # Limitar que el usuario solo pueda editar sus propios datos
    def has_change_permission(self, request, obj=None):
        # Si es superuser, puede editar a todos
        if request.user.is_superuser:
            return True
        # Si no es superuser, solo puede editar su propio registro
        if obj is not None and obj.id != request.user.id:
            return False
        return True


    list_filter = (
        'first_name',
        'last_name',
        'trabajo'
    )

    search_fields = (
        'first_name',
        'last_name',
        'trabajo',
        'dni'
    )

class PuestoAdmin (admin.ModelAdmin):
    list_display=(
        'puesto_Nombre',
        'producto_Psiquiatrico',
    )
    
class ProveedorAdmin (admin.ModelAdmin):
    list_display=(
        'nombre',
        
    )
    
    list_filter=(
        'nombre',
    )   

class LaboratorioAdmin (admin.ModelAdmin):
    list_display=(
        'nombre',
    )
    
    list_filter=(
        'nombre',
    )   

class PacienteAdmin (admin.ModelAdmin):
    list_display=(
        'nombre',
        'apellido',
        'dni',
    )
    
    
    
    list_filter=(
        'nombre',
        'apellido',
        
    )
    
    search_fields=(
        'nombre',
        'apellido',
        'dni'
    )


class ContactoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Telefono', {
            'fields': ('numero_Telefono', 'numero_Opcional'),
        }),
        ('Dirección', {
            'fields': ('calle', 'número', 'piso', 'departamento', 'localidad', 'código_Postal'),
        }),
        ('Email', {
            'fields': ('email',),
        }),
    )
    
        
class ProvinciaAdmin (admin.ModelAdmin):
    list_display= [
        'nombre',
        ]
    
    list_filter=[
        'nombre',
    ]
    
class LocalidadesAdmin (admin.ModelAdmin):
    list_display= [
        'nombre',
        ]
    
    list_filter=[
        'nombre',
    ]

    
    
admin.site.register(Empleado,EmpleadoAdmin)
admin.site.register(Puesto, PuestoAdmin)
admin.site.register(Proveedor,ProveedorAdmin)
admin.site.register(Paciente,PacienteAdmin)
admin.site.register(Laboratorio,LaboratorioAdmin)
admin.site.register(contacto, ContactoAdmin)
admin.site.register(provincia, ProvinciaAdmin)
admin.site.register(localidad, LocalidadesAdmin)


