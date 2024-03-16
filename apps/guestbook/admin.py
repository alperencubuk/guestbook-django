from django.contrib import admin

from apps.guestbook.models import Entry, User

admin.site.register(Entry)
admin.site.register(User)
