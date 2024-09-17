from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q
from drf_yasg.utils import swagger_auto_schema
from .models import Department, Employee
from .serializers import EmployeeSerializer, DepartmentSerializer
from  djangotest.tasks import add_employee_task, add

class UserView(APIView):
    @swagger_auto_schema(request_body=EmployeeSerializer)
    def post(self, request):

        serializer = EmployeeSerializer(data=request.data)

        if serializer.is_valid():
            full_name = serializer.validated_data.get('full_name', '').split()
            if len(full_name) < 2:
                return Response({"error": "Invalid full_name"}, status=status.HTTP_400_BAD_REQUEST)
            
            first_name = full_name[0]
            last_name = full_name[1]
            middle_name = full_name[2] if len(full_name) > 2 else None
            department_name = serializer.validated_data.get('department')
            gender = serializer.validated_data.get('gender')
            
            gender_value = 1 if gender == 'мужской' else 2
            #add.delay(3, 5)
            # Запускаем асинхронную задачу для создания сотрудника(отдела)
            add_employee_task.delay(first_name, last_name, middle_name, department_name, gender_value)

            return Response({"status": "Task received"}, status=status.HTTP_200_OK)

    def get(self, request):
        departments = Department.objects.annotate(
            employee_count=Count('employee'),
            male_count=Count('employee', filter=Q(employee__gender=1)),
            female_count=Count('employee', filter=Q(employee__gender=2))
        )
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)
