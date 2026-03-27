from django import forms
from .models import Part


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = '__all__'
        labels = {
            'project': 'Proyecto',
            'part_number': 'Número de parte',
            'part_date': 'Fecha del parte',
            'canal': 'Canal',
            'responsible_employee': 'Empleado responsable',
            'substitute_responsible': 'Responsable sustituto',
            'substitute_start_time': 'Hora inicio sustituto',
            'substitute_end_time': 'Hora fin sustituto',
            'ground': 'Terreno',
            'excess_hours_justified': 'Horas extra justificadas',
            'status': 'Estado',
            'is_deleted': 'Eliminado',
        }
        widgets = {
            'part_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'substitute_start_time': forms.TimeInput(
                attrs={'type': 'time', 'class': 'form-control'}
            ),
            'substitute_end_time': forms.TimeInput(
                attrs={'type': 'time', 'class': 'form-control'}
            ),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'part_number': forms.TextInput(attrs={'class': 'form-control'}),
            'canal': forms.Select(attrs={'class': 'form-control'}),
            'responsible_employee': forms.Select(attrs={'class': 'form-control'}),
            'substitute_responsible': forms.Select(attrs={'class': 'form-control'}),
            'ground': forms.Select(attrs={'class': 'form-control'}),
            'excess_hours_justified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'is_deleted': forms.HiddenInput(),
        }
