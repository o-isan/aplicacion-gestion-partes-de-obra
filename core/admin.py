from django.contrib import admin
from .models import (
    Employee, Project, Canal, Ground,
    Machineries, ExcessHoursReasons,
    Part, PartMachinery, ExcessHoursJustification,
)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')
    search_fields = ('name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    search_fields = ('name',)


@admin.register(Canal)
class CanalAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(Ground)
class GroundAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Machineries)
class MachineriesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(ExcessHoursReasons)
class ExcessHoursReasonsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('part_number', 'project', 'part_date', 'status', 'is_deleted')
    list_filter = ('status', 'is_deleted')
    search_fields = ('part_number',)


@admin.register(PartMachinery)
class PartMachineryAdmin(admin.ModelAdmin):
    list_display = ('part', 'machinery', 'hours_used')


@admin.register(ExcessHoursJustification)
class ExcessHoursJustificationAdmin(admin.ModelAdmin):
    list_display = ('part', 'reason')
