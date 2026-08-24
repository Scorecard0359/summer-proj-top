from django.contrib import admin
from .models import Task, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

@admin.register(Task)
class TasksAdmin(admin.ModelAdmin):
    list_display = ["title", "category_task", "is_completed", "created_date"]
    list_filter = ["is_completed", "category_task", "created_date"]
    search_fields = ["title", "description"]
    ordering = ["-created_date"]
