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

        return render(request, "todoapp/index.html", context=context)

class TaskListView(ListView):
    """
    1. ListView - получает все объекты модели (.objects.all())
    2. Позволяет передавать в шаблон
    """

    model = Task
    temp_name = "task_list.html"
    context_object_name = "tasks" # ? В шаблоне мы будем обращаться {{ tasks }}
    ordering = ['is_completed', '-created_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_task_id = self.request.GET.get('category')

        if category_task_id:
            context['category'] = Category.objects.filter(id=category_task_id).first()

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        category_task_id = self.request.GET.get('category')

        if category_task_id:
            queryset = queryset.filter(category_task_id=category_task_id)

        return queryset

class TaskDetailView(DetailView):
    """
    1. DetailView - автоматически выбирает объект по PK (первичный ключ)
    2. Автоматически передаёт всё в шаблон
    """

    model = Task
    # temp_name = "task_detail.html"
    # context_object_name = "task" # ? В шаблоне мы будем обращаться {{ task }}
    # url = reverse_lazy('todo:task_list')

    # def form_valid(self, form):
    #     title = form.cleaned_data['title']

    #     if Task.objects.filter(title=title).exists():
    #         message.warning(self.request, "Задача существует")

    #     return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

    #     context['category_task'] = Category.objects.all()

    #     return context
