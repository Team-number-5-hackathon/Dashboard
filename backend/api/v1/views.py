from django.db.models import Avg, CharField, Count, F, IntegerField, Q, Value
from django.db.models.functions import Cast, Concat
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from api.v1.filters import RatingFilter
from api.v1.serializers import (CompetenceSerializer, DomainSerializer,
                                EmployeesCountWithSkillsSerializer,
                                EmployeesWithSkillSerializer,
                                EmployeeGradesSerializer,
                                EmployeePositionsSerializer,
                                EmployeeSerializer,
                                EmployeeSkillAverageRatingSerializer,
                                PositionSerializer, RatingSerializer,
                                SkillsDevelopmentSerializer, SkillSerializer,
                                SuitabilityPositionSerializer, TeamSerializer)
from employees.models import Employee, Position, Team
from ratings.models import Competence, Domain, Rating, Skill


class PositionViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с должностями."""

    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    ordering_fields = "name"


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с командами."""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    ordering_fields = "name"


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с сотрудниками."""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    ordering_fields = "name"


class DomainViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с доменами."""

    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    ordering_fields = "name"


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с навыками."""

    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    ordering_fields = "name"


class CompetenceViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с компетенциями."""

    queryset = Competence.objects.all()
    serializer_class = CompetenceSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    ordering_fields = "name"


class RatingViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с оценками сотрудников."""

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = RatingFilter

# --------------------------------------------
#    Чарт 1 Вкладка 1
# --------------------------------------------


class SuitabilityPositionViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    """Вьюсет для работы с чартом "Соответствие должности"."""

    serializer_class = SuitabilityPositionSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = RatingFilter

    def get_queryset(self):
        return (
            Rating.objects.all()
            .select_related("employee")
            .values(
                "employee__id",
                full_name=Concat(
                    "employee__last_name", Value(" "), "employee__first_name"
                )
            )
            .annotate(
                total=Count(
                    "skill",
                    distinct=True,
                    filter=~Q(suitability="не требуется"),
                ),
                total_yes=Count(
                    "skill", distinct=True, filter=Q(suitability="да")
                ),
                percentage=Cast(
                    F("total_yes") * 100.0 / F("total"),
                    output_field=IntegerField(),
                ),
            )
            .order_by("percentage")
        )


class EmployeeSkillsAverageRatingViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    """Вьюсет для работы с чартом "Уровень владения навыками"."""

    serializer_class = EmployeeSkillAverageRatingSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RatingFilter

    def get_queryset(self):
        # Получаем employee_id из URL
        employee_id = self.kwargs.get("employee_id")

        # Проверяем, существует ли сотрудник с этим employee_id
        employeee = get_object_or_404(Employee, id=employee_id)

        # Группируем данные по навыкам и
        # считаем среднюю оценку для каждого навыка
        return (
            Rating.objects.filter(employee_id=employee_id)
            .values("skill__name")
            .annotate(average_rating=Avg("rating_value"))
            .order_by("average_rating")
        )

# --------------------------------------------
#    Чарт 1 Вкладка 2
# --------------------------------------------


class EmployeesCountWithSkillsViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Вьюсет для чарта "Колличество сотрудников, владеющих навыком"
     для ВСЕХ НАВЫКОВ.
    """

    serializer_class = EmployeesCountWithSkillsSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = RatingFilter

    def get_queryset(self):
        return Rating.objects.select_related(
            "skill"
        ).filter(
            suitability="да"
        ).values(
            "skill__id",
            "skill__name",
            "skill__competence__domain__name",
        ).annotate(
            skill_employee_count=Count(
                "employee",
                distinct=True,
            )
        ).order_by(
            "skill_employee_count"
        )


class EmployeesWithSkillViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для чарта "Колличество сотрудников, владеющих навыком"
     для ВЫБРАННОГО НАВЫКА.
    """

    serializer_class = EmployeesWithSkillSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = RatingFilter

    def get_queryset(self):
        skill = get_object_or_404(Skill, id=self.kwargs.get("skill_id"))
        return Rating.objects.select_related(
            "employee",
            "skill",
            "skill__competence",
            "skill__competence__domain"
        ).filter(
            suitability="да",
            skill=skill
        ).values(
            "skill__competence__domain__name"
        ).annotate(
            full_name=Concat(
                "employee__last_name",
                Value(" "),
                "employee__first_name",
                output_field=CharField()
            ),
            skill_employee_count=Count(
                "employee",
                distinct=True
            )
        ).order_by(
            "full_name"
        )

# --------------------------------------------
#    Чарт 2 Вкладка 1
# --------------------------------------------


class EmployeePositionsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Вьюсет для работы с чартом "Должности сотрудников"."""

    serializer_class = EmployeePositionsSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = RatingFilter

    def get_queryset(self):
        queryset = (
            Rating.objects.all()
            .select_related("employee")
            .values(
                "employee__position__name",
            )
            .annotate(
                position_employee_count=Count(
                    "employee",
                    distinct=True,
                )
            )
            .order_by(
                "position_employee_count",
            )
        )
        filtered_queryset = self.filter_queryset(queryset)
        total_employee_count = sum(
            item["position_employee_count"] for item in filtered_queryset
        )

        return filtered_queryset.annotate(
            total_employee_count=Value(
                total_employee_count, output_field=IntegerField()
            )
        )

# --------------------------------------------
#    Чарт 2 Вкладка 2
# --------------------------------------------


class EmployeeGradesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Вьюсет для работы с чартом "Количество сотрудников по грейдам"."""

    serializer_class = EmployeeGradesSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = RatingFilter

    def get_queryset(self):
        queryset = (
            Rating.objects.all()
            .select_related("employee")
            .values(
                "employee__grade",
            )
            .annotate(
                grade_employee_count=Count(
                    "employee",
                    distinct=True,
                )
            )
            .order_by(
                "grade_employee_count",
            )
        )
        filtered_queryset = self.filter_queryset(queryset)
        total_employee_count = sum(
            item["grade_employee_count"] for item in filtered_queryset
        )

        return filtered_queryset.annotate(
            total_employee_count=Value(
                total_employee_count, output_field=IntegerField()
            )
        )

# --------------------------------------------
#    Чарт 4 Вкладка 1
# --------------------------------------------


class SkillsDevelopmentViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Вьюсет для работы с чартом "Развитие навыков"."""

    serializer_class = SkillsDevelopmentSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = RatingFilter

    def get_queryset(self):
        return (
            Rating.objects.all()
            .select_related("skill")
            .values("rating_date")
            .annotate(
                average_rating=Avg("rating_value"),
                average_rating_hard=Avg(
                    "rating_value",
                    filter=Q(skill__competence__domain__name="Hard skills"),
                ),
                average_rating_soft=Avg(
                    "rating_value",
                    filter=Q(skill__competence__domain__name="Soft skills"),
                ),
            )
            .order_by("rating_date")
        )
