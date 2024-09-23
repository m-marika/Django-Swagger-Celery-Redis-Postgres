from django.contrib import admin
from .models import Department, Employee
from django.http import HttpRequest

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """
    Класс для настройки админки модели Employee.
    """

    # Поля, которые будут отображаться в списке сотрудников в админке
    list_display = ('first_name', 'last_name', 'middle_name', 'gender', 'department', 'created_at')
    # Поля, по которым можно искать сотрудников
    search_fields = ('first_name', 'last_name', 'middle_name')
    # Фильтры для списка сотрудников по полу и дате создания
    list_filter = ('gender', 'created_at')

    def has_add_permission(self, request: HttpRequest) -> bool:
        """
        Отключаем возможность добавления новых сотрудников через админку.
        :param request: Запрос, инициирующий проверку.
        :return: False, чтобы запретить добавление новых записей.
        """
        return False


class EmployeeInline(admin.TabularInline):
    """
    Класс для отображения сотрудников как inline в админке при редактировании отдела.
    """
    
    model = Employee  # Модель сотрудника, которую будем отображать
    extra = 1  # Количество пустых строк для ввода новых сотрудников (1 по умолчанию)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """
    Класс для настройки админки модели Department.
    """

    # Поля, которые будут отображаться в списке отделов в админке
    list_display = ('name',)
    # Поля, по которым можно искать отделы
    search_fields = ('name',)
    # Связь с моделью Employee для отображения сотрудников внутри отдела
    inlines = [EmployeeInline]

    def has_add_permission(self, request: HttpRequest) -> bool:
        """
        Отключаем возможность добавления новых отделов через админку.
        :param request: Запрос, инициирующий проверку.
        :return: False, чтобы запретить добавление новых записей.
        """
        return False
