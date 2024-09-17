from rest_framework import serializers
from .models import Employee, Department

class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)
    department = serializers.CharField()
    
    class Meta:
        model = Employee
        fields = ['full_name', 'department', 'gender', 'created_at']
        read_only_fields = ['created_at']


class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.IntegerField(read_only=True)
    male_count = serializers.IntegerField(read_only=True)
    female_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'employee_count', 'male_count', 'female_count']
