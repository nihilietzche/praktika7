from django.contrib import admin
from .models import Test, Question, Category, Profile, Result
from .forms import ProfileForm



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name')
    form = ProfileForm


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1



class TestAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'visible',
        'max_points',
        'category',
    )
    inlines = [
    QuestionInline,
    ]

class  QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'question_text',
        'question_point',
    )

class  ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'external_id',
        'name',
    )

class ResultAdmin(admin.ModelAdmin):
    list_display = (
        'external_id',
        'title',
        'max_points',
        'points',
    )

admin.site.register(Result, ResultAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Category)
