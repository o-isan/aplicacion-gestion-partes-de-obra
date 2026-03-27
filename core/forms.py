from django import forms
from .models import (
    Part, Machineries, ExcessHoursReasons,
    ExcessHoursJustification, PartMachinery,
)


class PartForm(forms.ModelForm):
    """
    ModelForm for Part that also handles related ExcessHoursJustification
    and PartMachinery records. Business logic is delegated to
    Part.save_with_related().
    """

    # ── Extra fields for justification ──
    justification_reason = forms.ModelChoiceField(
        queryset=ExcessHoursReasons.objects.all(),
        required=False,
        label='Motivo de horas extra',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    justification_text = forms.CharField(
        required=False,
        label='Texto de justificación',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Describa la justificación de las horas extra...',
        }),
    )

    # ── Extra field for machinery ──
    machineries = forms.ModelMultipleChoiceField(
        queryset=Machineries.objects.all(),
        required=False,
        label='Maquinaria',
        widget=forms.SelectMultiple(attrs={'class': 'form-control form-select-multiple'}),
    )

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
            'excess_hours_justified': forms.CheckboxInput(
                attrs={'class': 'form-check-input', 'id': 'id_excess_hours_justified'}
            ),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'is_deleted': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate initial values when editing an existing Part
        if self.instance and self.instance.pk:
            justification = self.instance.excesshoursjustification_set.first()
            if justification:
                self.fields['justification_reason'].initial = justification.reason_id
                self.fields['justification_text'].initial = justification.justification_text

            machinery_ids = self.instance.partmachinery_set.values_list(
                'machinery_id', flat=True
            )
            self.fields['machineries'].initial = list(machinery_ids)

    def clean(self):
        cleaned_data = super().clean()
        excess = cleaned_data.get('excess_hours_justified', False)
        reason = cleaned_data.get('justification_reason')
        text = cleaned_data.get('justification_text', '').strip()

        if excess and not text:
            self.add_error(
                'justification_text',
                'Debe proporcionar un texto de justificación cuando las horas extra están justificadas.',
            )
        return cleaned_data

    def save(self, commit=True):
        part = super().save(commit=False)
        if commit:
            cleaned = self.cleaned_data
            machinery_ids = [m.pk for m in cleaned.get('machineries', [])]

            justification_data = None
            if cleaned.get('excess_hours_justified'):
                reason = cleaned.get('justification_reason')
                justification_data = {
                    'reason_id': reason.pk if reason else None,
                    'justification_text': cleaned.get('justification_text', ''),
                }

            part.save_with_related(
                machinery_ids=machinery_ids,
                justification_data=justification_data,
            )
        return part
