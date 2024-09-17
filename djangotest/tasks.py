import logging
from celery import shared_task
from users.models import Department, Employee

logger = logging.getLogger(__name__)

@shared_task
def add_employee_task(first_name, last_name, middle_name, department_name, gender_value):
    logger.info("Task started.")
    try:
        department, _ = Department.objects.get_or_create(name=department_name)
        logger.info(f"department= {department}")
        
        employee = Employee.objects.create(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            department=department,
            gender=gender_value,
        )
        logger.info(f"Employee created with id: {employee.id}")
        return employee.id
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

@shared_task
def add(a, b):
    print("add(a, b)=", a+b)
    logger.info("Task started.")
    return a+b
