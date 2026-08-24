from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Task, Category

class IndexView(View):

    def get(request):

        tasks = Task.objects.all()

        total_tasks = tasks.count()
        completed_tasks = tasks.filter(is_completed=True).count()
        pending_tasks = total_tasks - completed_tasks

        categories = Category.objects.all()

        context = {
            "tasks": tasks,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "categories": categories
        }

        return render(request, "index.html", context=context)

class TaskListView(ListView):
    """
    1. ListView - получает все объекты модели (.objects.all())
    2. Позволяет передавать в шаблон
    """

    MODEL = Task
    TEMP_NAME = "task_list.html"
    CONTEXT_OBJECT_NAME = "tasks" # ? В шаблоне мы будем обращаться {{ tasks }}
    ORDERING = ['is_completed', '-created_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tasks = context['tasks']
        context['total_tasks'] = tasks.count()
        context['completed_tasks'] = tasks.filter(is_completed=True).count()
        context['pending_tasks'] = context['total_tasks'] - context['completed_tasks']
        categories = Category.objects.all()

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        category_id = self.request.GET.get('category')

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

class TaskDetailView(DetailView):
    """
    1. DetailView - автоматически выбирает объект по PK (первичный ключ)
    2. Автоматически передаёт всё в шаблон
    """

    MODEL = Task
    TEMP_NAME = "task_detail.html"
    CONTEXT_OBJECT_NAME = "task" # ? В шаблоне мы будем обращаться {{ task }}
    URL = reverse_lazy('todo:task_list')

    def form_valid(self, form):
        title = form.cleaned_data['title']

        if Task.objects.filter(title=title).exists():
            message.warning(self.request, "Задача существует")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = "Создать новую задачу"
        context['category_task'] = Category.objects.all()

        return context

    # def get_queryset(self):
    #     queryset = super().get_queryset()

    #     task_id = self.request.GET.get('task')

    #     if task_id:
    #         queryset = queryset.filter(task_id=task_id)
    #         if not queryset.values("title"):
    #             return messages.warning(request, "Title is empty.")
    #         elif not queryset.values("category_task"):
    #             return messages.warning(request, "Category not set.")

    #     return queryset
