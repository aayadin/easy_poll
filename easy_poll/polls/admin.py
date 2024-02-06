from django.contrib import admin

from .models import Answer, Option, Poll, Question


class PollAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'pub_date'
    )


class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'poll',
        'text'
    )
    list_filter = (
        'poll',
    )


class OptionAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'text'
    )
    list_filter = (
        'question__poll',
        'question'
    )


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Answer)
