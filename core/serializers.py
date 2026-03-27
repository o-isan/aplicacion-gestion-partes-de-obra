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


# ─── Writable nested input serializers ──────────────────────────────

class JustificationInputSerializer(serializers.Serializer):
    reason_id = serializers.IntegerField(required=False, allow_null=True)
    justification_text = serializers.CharField()


class PartSerializer(serializers.ModelSerializer):
    # Read-only nested output
    partmachinery_set = PartMachinerySerializer(many=True, read_only=True)
    excesshoursjustification_set = ExcessHoursJustificationSerializer(
        many=True, read_only=True
    )

    # Writable input fields
    machinery_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        write_only=True,
    )
    justification = JustificationInputSerializer(
        required=False,
        write_only=True,
        allow_null=True,
    )

    class Meta:
        model = Part
        fields = '__all__'

    def create(self, validated_data):
        machinery_ids = validated_data.pop('machinery_ids', [])
        justification_data = validated_data.pop('justification', None)

        part = Part(**validated_data)
        part.save_with_related(
            machinery_ids=machinery_ids,
            justification_data=justification_data,
        )
        return part

    def update(self, instance, validated_data):
        machinery_ids = validated_data.pop('machinery_ids', None)
        justification_data = validated_data.pop('justification', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # If excess_hours_justified is False, clear justification
        if not instance.excess_hours_justified:
            justification_data = None

        instance.save_with_related(
            machinery_ids=machinery_ids,
            justification_data=justification_data,
        )
        return instance
