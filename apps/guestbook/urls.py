from django.urls import path

from apps.guestbook.views import EntryView, UserView

urlpatterns = [
    path("entries/", EntryView.as_view(), name="entry"),
    path("users/", UserView.as_view(), name="user"),
]
