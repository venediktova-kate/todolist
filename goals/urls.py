from django.urls import path

from goals import views

urlpatterns = [
    path("goal_category/create", views.GoalCategoryCreateView.as_view(), name='create_category'),
    path("goal_category/list", views.GoalCategoryListView.as_view(), name='list_category'),
    path('goal_category/<int:id>', views.GoalCategoryDetailsView.as_view(), name='category_details'),

    path("goal/create", views.GoalCreateView.as_view(), name='create_goal'),
    path("goal/list", views.GoalListView.as_view(), name='list_goal'),
    path('goal/<int:id>', views.GoalDetailsView.as_view(), name='goal_details'),
]
