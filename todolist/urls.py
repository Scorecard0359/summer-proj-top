from django.contrib import admin
from django.urls import path
from todoapp import views as todo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', todo.IndexView.get),
    path('task/', todo.TaskListView.as_view()),
    path('task/<int:pk>', todo.TaskDetailView.as_view()),
]
