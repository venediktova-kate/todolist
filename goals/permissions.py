from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView

from goals.models import GoalCategory, Goal, GoalComment, BoardParticipant


class GoalCategoryPermission(IsAuthenticated):

    def has_object_permission(self, request: Request, view: GenericAPIView, obj: GoalCategory) -> bool:
        return request.user == obj.user


class GoalPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj: Goal):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user_id=request.user.id, board_id=obj.category.board_id
            ).exists()
        return BoardParticipant.objects.filter(
            user_id=request.user.id, board_id=obj.category.board_id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        ).exists()


class CommentPermissions(IsAuthenticated):
    def has_permission(self, request, view):
        return BoardParticipant.objects.filter(
                user_id=request.user.id, board_id=Goal.objects.get(id=request.data["goal"]).category.board_id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
            ).exists()


class BoardPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()
