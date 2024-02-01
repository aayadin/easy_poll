from django.contrib import admin

from .models import Poll, Question


class PollAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'pub_date'
    )


admin.site.register(Poll, PollAdmin)
admin.site.register(Question)
