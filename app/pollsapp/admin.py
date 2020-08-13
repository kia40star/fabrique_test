from django.contrib import admin

from pollsapp.models import Poll, Question


class PollAdmin(admin.ModelAdmin):
    model = Poll


class QuestionAdmin(admin.ModelAdmin):
    model = Question


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
