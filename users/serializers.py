from rest_framework import serializers
from .models import Employee, Department
from typing import Optional


class EmployeeSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField(write_only=True)
    department = serializers.CharField()
    
    # Поле для отображения значения гендера в виде строки (например, "Мужской" или "Женский")
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    # Поле для ввода числового значения гендера (1 для мужского, 2 для женского)
    gender = serializers.ChoiceField(choices=Employee.GENDER)

    class Meta:
        model = Employee
        fields = ['full_name', 'department', 'gender', 'gender_display', 'created_at']
        read_only_fields = ['created_at']

    def validate_full_name(self, value: str) -> str:
        """
        Валидация поля полного имени. Проверяем, что введено хотя бы два слова: имя и фамилия.
        :param value: Введённое значение полного имени.
        :return: Введённое значение, если оно валидно.
        """
        full_name = value.split()
        if len(full_name) < 2:
            raise serializers.ValidationError("Invalid full_name: имя и фамилия обязательны.")
        return value

    def validate_department(self, value: str) -> str:
        """
        Валидация поля department. Проверяем, что название отдела не является пустым.
        :param value: Введённое название отдела.
        :return: Введённое значение, если оно валидно.
        """
        if not value.strip():  # Проверяем, что строка не состоит только из пробелов
            raise serializers.ValidationError("Department name is required.")
        return value


class DepartmentSerializer(serializers.ModelSerializer):
    # Поля для подсчёта сотрудников в каждом отделе, а также для разделения по полу
    employee_count = serializers.IntegerField(read_only=True)
    male_count = serializers.IntegerField(read_only=True)
    female_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'employee_count', 'male_count', 'female_count']
