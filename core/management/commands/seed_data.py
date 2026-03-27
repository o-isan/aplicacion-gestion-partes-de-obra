from django.core.management.base import BaseCommand
from core.models import (
    Employee, Project, Canal, Ground,
    Machineries, ExcessHoursReasons,
)


class Command(BaseCommand):
    help = 'Seed the database with initial reference data for all lookup tables.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # ── Employees ──
        employees = [
            {'name': 'Juan García', 'role': 'Capataz'},
            {'name': 'María López', 'role': 'Ingeniera de obra'},
            {'name': 'Carlos Martínez', 'role': 'Operador de maquinaria'},
            {'name': 'Ana Rodríguez', 'role': 'Topógrafa'},
            {'name': 'Pedro Sánchez', 'role': 'Peón especializado'},
            {'name': 'Laura Fernández', 'role': 'Jefa de obra'},
        ]
        for e in employees:
            Employee.objects.get_or_create(name=e['name'], defaults=e)

        # ── Projects ──
        projects = [
            {
                'name': 'Modernización Canal Imperial',
                'description': 'Obras de modernización del Canal Imperial de Aragón',
            },
            {
                'name': 'Reparación Acequia Mayor',
                'description': 'Reparación y mejora de la Acequia Mayor del Ebro',
            },
            {
                'name': 'Nuevo Tramo Canal del Cinca',
                'description': 'Construcción de nuevo tramo en el Canal del Cinca',
            },
            {
                'name': 'Mantenimiento Red Secundaria',
                'description': 'Mantenimiento preventivo de la red secundaria de riego',
            },
        ]
        for p in projects:
            Project.objects.get_or_create(name=p['name'], defaults=p)

        # ── Canales ──
        canales = [
            {'code': 'CI-001', 'name': 'Canal Imperial'},
            {'code': 'AM-002', 'name': 'Acequia Mayor'},
            {'code': 'CC-003', 'name': 'Canal del Cinca'},
            {'code': 'RS-004', 'name': 'Red Secundaria Norte'},
            {'code': 'RS-005', 'name': 'Red Secundaria Sur'},
        ]
        for c in canales:
            Canal.objects.get_or_create(code=c['code'], defaults=c)

        # ── Grounds ──
        grounds = [
            {'name': 'Arcilla', 'description': 'Terreno arcilloso compacto'},
            {'name': 'Arena', 'description': 'Terreno arenoso suelto'},
            {'name': 'Roca', 'description': 'Terreno rocoso o pedregoso'},
            {'name': 'Tierra vegetal', 'description': 'Capa superficial con materia orgánica'},
            {'name': 'Grava', 'description': 'Terreno con predominancia de grava'},
        ]
        for g in grounds:
            Ground.objects.get_or_create(name=g['name'], defaults=g)

        # ── Machineries ──
        machineries = [
            {'name': 'Retroexcavadora CAT 320'},
            {'name': 'Pala cargadora Volvo L120'},
            {'name': 'Camión volquete MAN TGS'},
            {'name': 'Rodillo compactador Bomag'},
            {'name': 'Motoniveladora Komatsu GD655'},
            {'name': 'Grúa móvil Liebherr LTM 1060'},
            {'name': 'Dumper articulado Bell B30'},
        ]
        for m in machineries:
            Machineries.objects.get_or_create(name=m['name'], defaults=m)

        # ── ExcessHoursReasons ──
        reasons = [
            {
                'name': 'Condiciones meteorológicas',
                'description': 'Retrasos por lluvia, nieve o condiciones adversas',
            },
            {
                'name': 'Avería de maquinaria',
                'description': 'Tiempo extra por reparación de equipos en obra',
            },
            {
                'name': 'Urgencia operativa',
                'description': 'Trabajos urgentes para evitar daños mayores',
            },
            {
                'name': 'Falta de material',
                'description': 'Retraso en suministro de materiales',
            },
            {
                'name': 'Modificación del proyecto',
                'description': 'Cambios en las especificaciones durante la ejecución',
            },
        ]
        for r in reasons:
            ExcessHoursReasons.objects.get_or_create(name=r['name'], defaults=r)

        self.stdout.write(self.style.SUCCESS('Seed data loaded successfully.'))
