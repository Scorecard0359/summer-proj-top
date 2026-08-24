from django.db import models
from django.urls import reverse

class Category(models.Model):

    name = models.CharField(
        max_length=60,
        verbose_name="Название",
        help_text="Введите название категории"
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("todo: category", kwargs={"category_id": self.id})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

class Task(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Задача",
        help_text="Введите название задачи"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Описание",
        help_text="Введите описание задачи"
    )

    created_date = models.DateField(
        auto_now_add=True,
        verbose_name="Дата создания задачи"
    )

    due_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Срок выполнения",
        help_text="Укажите срок выполнения задачи"
    )

    is_completed = models.BooleanField(
        default=False,
        verbose_name="Выполнено",
        help_text="Выполнена ли задача"
    )

    category_task = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категория задачи",
        related_name="tasks"
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("todo: tasks", kwargs={"pk": self.id})

    def toggle_completed(self):
        self.is_completed = not self.is_completed
        self.save()

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ['is_completed', '-created_date']
