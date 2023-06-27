from django.contrib import admin
from .models import Mention, UserProfile, Hashtag, Shot, Comment
# Register your models here.
admin.site.register(Mention)
admin.site.register(UserProfile)
admin.site.register(Hashtag)
admin.site.register(Shot)
admin.site.register(Comment)