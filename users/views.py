from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q
from drf_yasg.utils import swagger_auto_schema
from .models import Department, Employee
from .serializers import EmployeeSerializer, DepartmentSerializer
from djangotest.tasks import add_employee_task
from typing import List, Dict

class UserView(APIView):
    @swagger_auto_schema(request_body=EmployeeSerializer)
    def post(self, request) -> Response:
        """
        Обрабатывает POST запрос для создания нового сотрудника. 
        Сначала валидирует данные, а затем передает их в асинхронную задачу для создания сотрудника и отдела.

        :param request: Входящий HTTP запрос с данными о сотруднике.
        :return: Ответ с подтверждением получения задачи или сообщением об ошибке.
        """
        # Инициализируем сериализатор с данными запроса
        serializer = EmployeeSerializer(data=request.data)

        # Если данные валидны, продолжаем обработку
        if serializer.is_valid():
            employee_data: Dict = serializer.validated_data

            # Разбиваем полное имя на части (имя, фамилия, отчество)
            full_name_parts: List[str] = employee_data.get('full_name').split()
            first_name: str = full_name_parts[0]
            last_name: str = full_name_parts[1]
            middle_name: str = full_name_parts[2] if len(full_name_parts) > 2 else None
            
            # Получаем название отдела и гендер из данных
            department_name: str = employee_data.get('department')
            gender: int = employee_data.get('gender')

            # Запускаем асинхронную задачу для создания сотрудника и отдела
            add_employee_task.delay(first_name, last_name, middle_name, department_name, gender)

            # Возвращаем подтверждение о получении задачи
            return Response({"status": "Task received"}, status=status.HTTP_200_OK)
        
        # В случае ошибки валидации возвращаем ошибки
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request) -> Response:
        """
        Обрабатывает GET запрос для получения списка всех отделов с количеством сотрудников,
        а также с распределением по гендеру.

        :param request: Входящий HTTP запрос.
        :return: Ответ с сериализованными данными по отделам.
        """
        # Аннотируем количество сотрудников и распределение по гендеру для каждого отдела
        departments = Department.objects.annotate(
            employee_count=Count('employee'),  # Общее количество сотрудников в отделе
            male_count=Count('employee', filter=Q(employee__gender=1)),  # Количество мужчин
            female_count=Count('employee', filter=Q(employee__gender=2))  # Количество женщин
        )
        
        # Сериализуем аннотированные данные
        serializer = DepartmentSerializer(departments, many=True)
        
        # Возвращаем сериализованные данные в ответе
        return Response(serializer.data)
