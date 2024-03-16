from logging import getLogger

from django.db import models, transaction
from django.db.models import Count, F, OuterRef, Subquery, Value
from django.db.models.functions import Concat
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.guestbook.models import Entry, User
from apps.guestbook.pagination import EntryPagination
from apps.guestbook.serializers import (
    EntryCreateRequestSerializer,
    EntryCreateResponseSerializer,
    EntryResponseSerializer,
    UserListResponseSerializer,
)

logger = getLogger("logger")


class EntryView(APIView):
    def post(self, request):
        serializer = EntryCreateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            with transaction.atomic():
                user, created = User.objects.get_or_create(name=data["name"])
                entry = Entry(
                    subject=data["subject"], message=data["message"], user=user
                )
                entry.save()
        except Exception as e:
            logger.error(e)
            return Response(
                data={"message": "An error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        data = {
            "user": user.name,
            "subject": entry.subject,
            "message": entry.message,
        }

        serializer = EntryCreateResponseSerializer(data)

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def get(self, request):
        entries = (
            Entry.objects.all()
            .order_by("-created_date")
            .select_related("user")
            .values("subject", "message", username=F("user__name"))
        )
        paginator = EntryPagination()
        page = paginator.paginate_queryset(entries, request)
        serializer = EntryResponseSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class UserView(APIView):
    def get(self, request):
        users = (
            User.objects.annotate(
                username=models.F("name"),
                total_message_count=Count("entry"),
                last_entry=Subquery(
                    Entry.objects.filter(user_id=OuterRef("pk"))
                    .order_by("-created_date")[:1]
                    .annotate(
                        last_entry=Concat(
                            "subject",
                            Value(" | "),
                            "message",
                            output_field=models.TextField(),
                        )
                    )
                    .values("last_entry")
                ),
            )
            .values(
                "username",
                "total_message_count",
                "last_entry",
            )
            .order_by("-id")
        )

        serializer = UserListResponseSerializer({"users": users})
        return Response(serializer.data)
