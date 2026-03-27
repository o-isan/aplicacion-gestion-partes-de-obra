from django.db import models


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

    def __str__(self):
        return f"Part {self.part_number} - {self.project.name}"


class PartMachinery(models.Model):
    part = models.ForeignKey(Part, on_delete=models.PROTECT)
    machinery = models.ForeignKey(Machineries, on_delete=models.PROTECT)
    hours_used = models.PositiveIntegerField(null=True, blank=True)


class ExcessHoursJustification(models.Model):
    part = models.ForeignKey(Part, on_delete=models.PROTECT)
    reason = models.ForeignKey(ExcessHoursReasons, on_delete=models.PROTECT, null=True)
    justification_text = models.TextField()
