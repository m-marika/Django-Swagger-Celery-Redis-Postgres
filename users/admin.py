from django.contrib import admin
from .models import Department, Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'middle_name', 'gender', 'department', 'created_at')
    search_fields = ('first_name', 'last_name', 'middle_name')
    list_filter = ('gender', 'created_at')

    def has_add_permission(self, request):
        return False

class EmployeeInline(admin.TabularInline):
    model = Employee
    extra = 1

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [EmployeeInline]

    def has_add_permission(self, request):
        return False
