from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'id')
    readonly_fields = ('created', 'updated')
    list_filter = ('is_deleted',)
    search_fields = ('title',)


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'id', 'category')
    readonly_fields = ('created', 'updated')
    search_fields = ('title', 'description')
    list_filter = ('status', 'priority')


@admin.register(GoalComment)
class GoalCommentAdmin(admin.ModelAdmin):
    ...
