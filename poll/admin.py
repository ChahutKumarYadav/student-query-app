from django.contrib import admin
from .models import PollQuestion, PollChoice

admin.site.register(PollQuestion)
admin.site.register(PollChoice)
