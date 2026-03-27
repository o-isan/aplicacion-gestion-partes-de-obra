from django.core.exceptions import ValidationError
from django.db import models, transaction


# ─── Custom Manager ─────────────────────────────────────────────────

class ActivePartManager(models.Manager):
    """Returns only non-deleted Parts."""

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


# ─── Reference Models ───────────────────────────────────────────────

class Employee(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    total_activities_min = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Canal(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ground(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Machineries(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ExcessHoursReasons(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# ─── Part Model ─────────────────────────────────────────────────────

class Part(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]

    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    part_number = models.CharField(max_length=50)
    part_date = models.DateField()
    registration_date_utc = models.DateTimeField(auto_now_add=True)

    canal = models.ForeignKey(Canal, on_delete=models.PROTECT, null=True)
    responsible_employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        null=True,
        related_name='responsible_parts'
    )
    substitute_responsible = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='substitute_parts'
    )
    substitute_start_time = models.TimeField(null=True, blank=True)
    substitute_end_time = models.TimeField(null=True, blank=True)

    ground = models.ForeignKey(Ground, on_delete=models.PROTECT, null=True)

    excess_hours_justified = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    is_deleted = models.BooleanField(default=False)

    # Managers
    objects = models.Manager()
    active_objects = ActivePartManager()

    def __str__(self):
        return f"Part {self.part_number} - {self.project.name}"

    def clean(self):
        super().clean()
        if not self.excess_hours_justified and self.pk:
            if self.excesshoursjustification_set.exists():
                raise ValidationError(
                    'No puede existir una justificación de horas extra '
                    'si el campo "Horas extra justificadas" es falso.'
                )

    def save_with_related(self, machinery_ids=None, justification_data=None):
        """
        Save the Part along with its related PartMachinery and
        ExcessHoursJustification records inside a single transaction.

        Args:
            machinery_ids: list of Machineries PKs to associate
            justification_data: dict with 'reason_id' and 'justification_text',
                                or None to clear justification
        """
        with transaction.atomic():
            self.save()

            # ── Sync ExcessHoursJustification ──
            if self.excess_hours_justified and justification_data:
                reason_id = justification_data.get('reason_id')
                text = justification_data.get('justification_text', '')
                justification = self.excesshoursjustification_set.first()
                if justification:
                    justification.reason_id = reason_id
                    justification.justification_text = text
                    justification.save()
                else:
                    ExcessHoursJustification.objects.create(
                        part=self,
                        reason_id=reason_id,
                        justification_text=text,
                    )
            else:
                # Remove any existing justification
                self.excesshoursjustification_set.all().delete()

            # ── Sync PartMachinery ──
            if machinery_ids is not None:
                self.partmachinery_set.all().delete()
                for mid in machinery_ids:
                    PartMachinery.objects.create(part=self, machinery_id=mid)


# ─── Related Models ─────────────────────────────────────────────────

class PartMachinery(models.Model):
    part = models.ForeignKey(Part, on_delete=models.PROTECT)
    machinery = models.ForeignKey(Machineries, on_delete=models.PROTECT)
    hours_used = models.PositiveIntegerField(null=True, blank=True)


class ExcessHoursJustification(models.Model):
    part = models.ForeignKey(Part, on_delete=models.PROTECT)
    reason = models.ForeignKey(ExcessHoursReasons, on_delete=models.PROTECT, null=True)
    justification_text = models.TextField()
