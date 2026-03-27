from rest_framework import serializers
from .models import (
    Employee, Project, Canal, Ground,
    Machineries, ExcessHoursReasons,
    Part, PartMachinery, ExcessHoursJustification,
)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class CanalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canal
        fields = '__all__'


class GroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ground
        fields = '__all__'


class MachineriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machineries
        fields = '__all__'


class ExcessHoursReasonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcessHoursReasons
        fields = '__all__'


class PartMachinerySerializer(serializers.ModelSerializer):
    class Meta:
        model = PartMachinery
        fields = '__all__'


class ExcessHoursJustificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcessHoursJustification
        fields = '__all__'


class PartSerializer(serializers.ModelSerializer):
    partmachinery_set = PartMachinerySerializer(many=True, read_only=True)
    excesshoursjustification_set = ExcessHoursJustificationSerializer(many=True, read_only=True)

    class Meta:
        model = Part
        fields = '__all__'
