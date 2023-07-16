from django.urls import path

from goals.views import GoalCategoryCreateView, GoalCategoryListView, GoalCategoryDetailsView, GoalCreateView, \
    GoalListView, GoalDetailsView, GoalCommentCreateView, GoalCommentListView, GoalCommentDetailsView

urlpatterns = [
    path("goal_category/create", GoalCategoryCreateView.as_view(), name='create_category'),
    path("goal_category/list", GoalCategoryListView.as_view(), name='list_category'),
    path('goal_category/<int:id>', GoalCategoryDetailsView.as_view(), name='category_details'),

    path("goal/create", GoalCreateView.as_view(), name='create_goal'),
    path("goal/list", GoalListView.as_view(), name='list_goal'),
    path('goal/<int:id>', GoalDetailsView.as_view(), name='goal_details'),

    path("goal_comment/create", GoalCommentCreateView.as_view(), name='create_comment'),
    path("goal_comment/list", GoalCommentListView.as_view(), name='list_comment'),
    path('goal_comment/<int:id>', GoalCommentDetailsView.as_view(), name='comment_details'),
]
