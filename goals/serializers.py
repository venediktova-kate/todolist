from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from core.models import User
from core.serializers import ProfileSerializer
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_board(self, value: Board) -> Board:
        """
        Проверка прав пользователя перед созданием категории
        """
        if not BoardParticipant.objects.filter(board_id=value.pk,
                                               user_id=self.context["request"].user.id,
                                               role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]):
            raise serializers.ValidationError("Permission Denied")
        return value


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')

    def validate_category(self, category: GoalCategory) -> GoalCategory:
        if category.is_deleted:
            raise ValidationError("Category not found")

        if self.context['request'].user != category.user:
            raise PermissionDenied

        return category


class GoalSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')

    def validate_category(self, goal: Goal) -> Goal:
        if goal.status == Goal.Status.archived:
            raise ValidationError("Goal not found")

        if self.context['request'].user != goal.user:
            raise PermissionDenied

        return goal


class GoalCommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)
    goal = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user', 'goal')


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(required=True, choices=BoardParticipant.Role.choices)
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True, required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    title = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated')

    def update(self, instance, validated_data: dict):

        with transaction.atomic():
            instance.participants.exclude(user=self.context["request"].user).delete()
            if 'participants' in validated_data.keys():
                for participant in validated_data["participants"]:
                    BoardParticipant.objects.create(
                        user_id=participant["user"].id,
                        role=participant["role"],
                        board_id=instance.pk
                    )

            if validated_data["title"]:
                instance.title = validated_data["title"]
                instance.save(update_fields=("title",))

        return instance


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ("id", "created", "updated")
