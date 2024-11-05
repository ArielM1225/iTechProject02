from django.contrib import admin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ExportMixin
from aplicaciones.Comunidad.models import Empleado, Proveedor, Paciente, contacto, Laboratorio, provincia, localidad, Puesto


class EmpleadoResource(resources.ModelResource):
    trabajo = fields.Field(
        column_name='trabajo',
        attribute='trabajo',
        widget=ForeignKeyWidget(Puesto, 'puesto_Nombre')
    )
    
    # Definición de nuevos campos para nombre y apellido
    nombre = fields.Field(
        column_name='nombre',
        attribute='first_name',  # Asigna el valor de first_name a nombre
    )
    apellido = fields.Field(
        column_name='apellido',
        attribute='last_name',  # Asigna el valor de last_name a apellido
    )

    class Meta:
        model = Empleado
        exclude = (
            'password', 
            'is_superuser', 
            'is_staff', 
            'last_login', 
            'date_joined', 
            'user_permissions', 
            'groups', 
            'is_active',
            'first_name',  # Excluye el campo original first_name
            'last_name'    # Ya no debería aparecer
        )
        export_order = (
            'id', 
            'username', 
            'nombre',  # Campo nuevo para nombre
            'apellido',  # Campo nuevo para apellido
            'email', 
            'dni', 
            'nacimiento', 
            'trabajo'  # Columna trabajo al final
        )


class EmpleadoAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = EmpleadoResource
    list_display = ('username', 'email', 'dni', 'first_name', 'last_name', 'trabajo', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'email', 'dni', 'trabajo')}),
        ('Contacto', {'fields': ('id_Contacto',)}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'groups')}),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return ['trabajo', 'groups',]
        return []


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.id != request.user.id:
            return False
        return True
    def has_delete_permission(self, request, obj=None):
        return False

    list_filter = ('first_name', 'last_name', 'trabajo')
    search_fields = ('first_name', 'last_name', 'trabajo', 'dni')


# Configuración de import-export para otros modelos
class ProveedorResource(resources.ModelResource):
    class Meta:
        model = Proveedor


class ProveedorAdmin(admin.ModelAdmin):
    resource_class = ProveedorResource
    list_display = ('nombre',)
    list_filter = ('nombre',)


class PacienteResource(resources.ModelResource):
    class Meta:
        model = Paciente


class PacienteAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = PacienteResource
    list_display = ('nombre', 'apellido', 'dni')
    list_filter = ('nombre', 'apellido')
    search_fields = ('nombre', 'apellido', 'dni')


class ContactoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Teléfono', {'fields': ('numero_Telefono', 'numero_Opcional')}),
        ('Dirección', {'fields': ('calle', 'número', 'piso', 'departamento', 'localidad', 'código_Postal')}),
        ('Email', {'fields': ('email',)}),
    )


class PuestoAdmin(admin.ModelAdmin):
    list_display = ('puesto_Nombre', 'producto_Psiquiatrico')


class LaboratorioAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    list_filter = ('nombre',)


class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    list_filter = ('nombre',)


class LocalidadesAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    list_filter = ('nombre',)


# Registro de modelos en admin
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Puesto, PuestoAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Laboratorio, LaboratorioAdmin)
admin.site.register(contacto, ContactoAdmin)
admin.site.register(provincia, ProvinciaAdmin)
admin.site.register(localidad, LocalidadesAdmin)


