from datetime import date

from django.db import models

from core.models import User


class BaseMode(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=True)


class GoalCategory(BaseMode):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    def __str__(self):
        return self.title


class Goal(BaseMode):
    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    title = models.CharField(verbose_name="Название", max_length=255)
    description = models.TextField(verbose_name="Описание", blank=True, max_length=255)
    category = models.ForeignKey(GoalCategory, verbose_name="Категория", on_delete=models.PROTECT, related_name='goals')
    due_date = models.DateField(verbose_name="Дедлайн", default=date.today, blank=True, null=True)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    status = ...
    priority = ...

    def __str__(self) -> str:
        return self.title
