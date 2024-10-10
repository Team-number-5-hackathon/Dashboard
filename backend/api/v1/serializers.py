from rest_framework import serializers

from employees.models import Employee, Position, Team
from ratings.models import Competence, Domain, Rating, Skill


class TeamSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с командами."""

    class Meta:
        model = Team
        fields = ("id", "name")


class PositionSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с должностями."""

    class Meta:
        model = Position
        fields = ("id", "name")


class EmployeeSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с сотрудниками."""

    team = serializers.StringRelatedField(
        source="team.name", read_only=True
    )
    position = serializers.StringRelatedField(
        source="position.name", read_only=True
    )

    class Meta:
        model = Employee
        fields = "__all__"


class DomainSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с доменами."""

    class Meta:
        model = Domain
        fields = ("id", "name")


class CompetenceSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с компетенциями."""

    class Meta:
        model = Competence
        fields = ("id", "name")


class SkillSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с навыками."""

    class Meta:
        model = Skill
        fields = ("id", "name")


class RatingSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с оценками."""

    employee = serializers.StringRelatedField(
        read_only=True
    )
    team = serializers.StringRelatedField(
        source="employee.team", read_only=True
    )
    position = serializers.StringRelatedField(
        source="employee.position", read_only=True
    )
    grade = serializers.StringRelatedField(
        source="employee.grade", read_only=True
    )
    skill = serializers.StringRelatedField(
        source="skill.name", read_only=True
    )
    # domain = serializers.StringRelatedField(
    #     source='skill.competence.domain', read_only=True
    # )

    class Meta:
        model = Rating
        fields = (
            "employee",
            "team",
            "grade",
            "position",
            "skill",
            # "domain",
            "rating_date",
            "rating_value",
            "suitability",
        )

# --------------------------------------------
#    Чарт 1 Вкладка 1
# --------------------------------------------


class SuitabilityPositionSerializer(serializers.ModelSerializer):
    """Сериализатор для чарта "Соответствие должности"."""

    employee_id = serializers.CharField(source="employee__id", read_only=True)
    employee = serializers.CharField(source="full_name", read_only=True)
    total_yes = serializers.IntegerField()
    total = serializers.IntegerField()
    percentage = serializers.FloatField()

    class Meta:
        model = Rating
        fields = ("employee_id",
                  "employee",
                  "total_yes",
                  "total",
                  "percentage"
                  )


class EmployeeSkillAverageRatingSerializer(serializers.ModelSerializer):
    """Сериализатор для чарта "Уровень владения навыками"."""

    skill_name = serializers.CharField(source="skill__name", read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Rating
        fields = ("skill_name", "average_rating")

# --------------------------------------------
#    Чарт 1 Вкладка 2
# --------------------------------------------


class EmployeesCountWithSkillsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чарта "Количество сотрудников,
    владеющих навыком" для ВСЕХ НАВЫКОВ.
    """

    domain = serializers.CharField(
        source="skill__competence__domain__name",
        read_only=True,
    )
    skill_id = serializers.CharField(
        source="skill__id",
        read_only=True,
    )
    skill_name = serializers.CharField(
        source="skill__name",
        read_only=True,
    )
    count_employees = serializers.IntegerField(
        source="skill_employee_count",
        read_only=True,
    )

    class Meta:
        model = Rating
        fields = (
            "domain",
            "skill_id",
            "skill_name",
            "count_employees",
        )


class EmployeesWithSkillSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чарта "Количество сотрудников,
    владеющих навыком" для ВЫБРАННОГО НАВЫКА.
    """

    domain = serializers.CharField(
        source="skill__competence__domain__name",
        read_only=True,
    )
    employee = serializers.CharField(
        source="full_name",
        read_only=True,
    )
    count_employees = serializers.IntegerField(
        source="skill_employee_count",
        read_only=True,
    )

    class Meta:
        model = Rating
        fields = (
            "domain",
            "employee",
            "count_employees",
        )

# --------------------------------------------
#    Чарт 2 Вкладка 1
# --------------------------------------------


class EmployeePositionsSerializer(serializers.ModelSerializer):
    """Сериализатор для чарта "Должности сотрудников"."""

    position = serializers.CharField(
        source="employee__position__name", read_only=True
    )
    position_employee_count = serializers.IntegerField(read_only=True)
    total_employee_count = serializers.IntegerField(read_only=True)
    percentage = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = (
            "position",
            "position_employee_count",
            "total_employee_count",
            "percentage",
        )

    def get_percentage(self, obj):
        return round(
            obj["position_employee_count"] * 100 / obj["total_employee_count"],
            1,
        )

# --------------------------------------------
#    Чарт 2 Вкладка 2
# --------------------------------------------


class EmployeeGradesSerializer(serializers.ModelSerializer):
    """Сериализатор для чарта "Количество сотрудников по грейдам"."""

    grade = serializers.CharField(
        source="employee__grade", read_only=True
    )
    grade_employee_count = serializers.IntegerField(read_only=True)
    total_employee_count = serializers.IntegerField(read_only=True)
    percentage = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = (
            "grade",
            "grade_employee_count",
            "total_employee_count",
            "percentage",
        )

    def get_percentage(self, obj):
        return round(
            obj["grade_employee_count"] * 100 / obj["total_employee_count"],
            1,
        )


class EmployeeGradesWithPositionsSerializer(serializers.ModelSerializer):
    """Сериализатор для чарта "Количество сотрудников по грейдам".
    для ВЫБРАННОГО ГРЕЙДА
    """

    position = serializers.CharField(
        source="employee__position__name", read_only=True
    )
    position_employee_count = serializers.IntegerField(read_only=True)
    total_employee_count = serializers.IntegerField(read_only=True)
    percentage = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = (
            "position",
            "position_employee_count",
            "total_employee_count",
            "percentage",
        )

    def get_percentage(self, obj):
        return round(
            obj["position_employee_count"] * 100 / obj["total_employee_count"],
            1,
        )

# --------------------------------------------
#    Чарт 4 Вкладка 1
# --------------------------------------------


class SkillsDevelopmentSerializer(serializers.ModelSerializer):
    """Сериализатор для чарта "Динамика развития навыков"."""

    rating_date = serializers.DateField()
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    average_rating_hard = serializers.DecimalField(
        max_digits=3, decimal_places=2
    )
    average_rating_soft = serializers.DecimalField(
        max_digits=3, decimal_places=2
    )

    class Meta:
        model = Rating
        fields = (
            "rating_date",
            "average_rating",
            "average_rating_hard",
            "average_rating_soft",
        )

# --------------------------------------------
#    Чарт 4 Вкладка 2
# --------------------------------------------


class PositionRatingSerializer(serializers.ModelSerializer):
    """Сериализатор для чарта "Оценки сотрудников по должностям"."""

    position = serializers.CharField(source="employee__position__name")
    position_id = serializers.CharField(source="employee__position__id")
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        model = Rating
        fields = (
            "position",
            "position_id",
            "average_rating",
        )


class GradeRatingSerializer(serializers.ModelSerializer):
    """Сериализатор для чарта "Оценки сотрудников по должностям".
    для ВЫБРАННОЙ ДОЛЖНОСТИ
    """
    grade = serializers.CharField(source="employee__grade")
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        model = Rating
        fields = (
            "grade",
            "average_rating",
        )


class EmployeeRatingSerializer(serializers.ModelSerializer):
    """Сериализатор для чарта "Оценки сотрудников по должностям".
    для ВЫБРАННОЙ ДОЛЖНОСТИ И ГРЕЙДА
    """

    employee = employee = serializers.CharField(
        source="full_name",
        read_only=True,
    )
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        model = Rating
        fields = (
            "employee",
            "average_rating",
        )
