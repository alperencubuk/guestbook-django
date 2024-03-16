from rest_framework.test import APITestCase

from apps.guestbook.models import Entry, User


def create_test_data():
    users = []
    for i in range(3):
        user = User.objects.create(name=f"User {i}")
        for j in range(3):
            Entry.objects.create(
                user=user,
                subject=f"Subject {j} by {user.name}",
                message=f"Message {j} by {user.name}",
            )
        users.append(user)
    return users


class EntryViewTests(APITestCase):
    def setUp(self):
        self.users = create_test_data()

    def test_entry_creation(self):
        data = {
            "name": "John Doe",
            "subject": "Test Subject",
            "message": "Test Message",
        }

        response = self.client.post("/guestbook/entries/", data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["user"], data["name"])
        self.assertEqual(response.data["subject"], data["subject"])
        self.assertEqual(response.data["message"], data["message"])

    def test_entry_list_pagination(self):
        response = self.client.get("/guestbook/entries/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 9)
        self.assertEqual(response.data["page_size"], 3)
        self.assertEqual(response.data["total_pages"], 3)
        self.assertEqual(response.data["current_page_number"], 1)
        self.assertEqual(len(response.data["entries"]), 3)


class UserViewTests(APITestCase):
    def setUp(self):
        self.users = create_test_data()

    def test_user_list(self):
        response = self.client.get("/guestbook/users/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["users"]), 3)

        for i, user_data in enumerate(reversed(response.data["users"])):
            user = self.users[i]
            self.assertEqual(user_data["username"], user.name)
            self.assertEqual(user_data["total_message_count"], 3)
            self.assertEqual(
                user_data["last_entry"],
                f"Subject 2 by {user.name} | Message 2 by {user.name}",
            )
