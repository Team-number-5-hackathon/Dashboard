from django.db import models

from backend.config import MAX_LENGTH, MIN_LENGTH
from backend.employees.models import Employee


class Domain(models.Model):
    """Модель домена."""

    name = models.CharField(
        max_length=MIN_LENGTH,
        verbose_name="Название домена",
        unique=True
    )

    class Meta:
        verbose_name = "Домен"
        verbose_name_plural = "Домены"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Competence(models.Model):
    """Модель компетенции."""

    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="Название компетенции",
        unique=True
    )
    domain = models.ForeignKey(
        Domain,
        on_delete=models.CASCADE,
        verbose_name="Домен",
        related_name="competencies"
    )

    class Meta:
        verbose_name = "Компетенция"
        verbose_name_plural = "Компетенции"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Skill(models.Model):
    """Модель навыка."""

    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name="Название навыка",
        unique=True
    )
    competence = models.ForeignKey(
        Competence,
        on_delete=models.CASCADE,
        verbose_name="Компетенция",
        related_name="skills"
    )

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"
        ordering = ("name",)

    def __str__(self):
        return self.name

class Rating(models.Model):
    """Модель оценки навыков сотрудников."""

    RATING_CHOICES = [i for i in range(1,6)]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name="Сотрудник",
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        verbose_name="Оцениваемый навык",
    )
    rating_date = models.DateField(
        verbose_name="Дата оценки",
    )
    rating_value = models.IntegerField(
        verbose_name="Оценка сотрудника",
        choices=RATING_CHOICES,
    )
    suitability = models.CharField(
        max_length=MIN_LENGTH,
        verbose_name="Соответствие",
    )

    class Meta:
        verbose_name = "Оценка навыков сотрудника"
        verbose_name_plural = "Оценки навыков сотрудников"
        default_related_name = "ratings"
        ordering = ("employee__last_name", "employee__first_name", "-rating_date",)

    def __str__(self):
        return self.name
