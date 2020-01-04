from django.contrib import admin
from .models import Device, Attribute, Value


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'mac')
    search_fields = ('name', '=address')


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('device', 'endpoint', 'cluster', 'number', 'name', 'unit', 'exponent')
    list_filter = ('device', )
    search_fields = ('name', )


@admin.register(Value)
class ValueAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'timestamp', 'value', 'fmt_value')
    list_filter = ('attribute', )
    date_hierarchy = 'timestamp'
