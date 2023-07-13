from django.urls import path

from goals import views
from goals.views import GoalCategoryDetailsView

urlpatterns = [
    path("goal_category/create", views.GoalCategoryCreateView.as_view(), name='create_category'),
    path("goal_category/list", views.GoalCategoryListView.as_view(), name='list_category'),
    path('goal_category/<int:id>', GoalCategoryDetailsView.as_view(), name='category_details'),
]
