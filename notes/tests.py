from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Note

# Create your tests here.

class NoteTests(TestCase):

    # test viewing the notes list
    def setUp(self):
        self.user = User.objects.create_user(username="jacob", password="test123")
        self.client.login(username="jacob", password="test123")
        self.note = Note.objects.create(
            title="Test Note",
            content="This is a test note.",
            category="General",
            user=self.user
        )

    def test_note_list_view(self):
        response = self.client.get(reverse("note_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Note")


# test creating a note
    def test_create_note(self):
        response = self.client.post(reverse("add_note"), {
            "title": "New Note",
            "content": "Created via test",
            "category": "Work"
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Note.objects.filter(title="New Note").exists()) 


# test edit note
    def test_edit_note(self):
        response = self.client.post(reverse("edit_note", args=[self.note.id]), {
            "title": "Updated Title",
            "content": "Updated content",
            "category": "Ideas"
        })
        self.assertEqual(response.status_code, 302)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Updated Title")


# test delete note
    def test_delete_note(self):
        response = self.client.post(reverse("delete_note", args=[self.note.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())  


# test category fields for notes
    def test_category_field(self):
        self.assertEqual(self.note.category, "General")



# test notes are tied to the user  
    def test_notes_are_user_specific(self):
        other_user = User.objects.create_user(username="other", password="pass123")
        Note.objects.create(
            title="Other User Note",
            content="Should not appear",
            category="Personal",
            user=other_user
        )

        response = self.client.get(reverse("note_list"))
        self.assertContains(response, "Test Note")
        self.assertNotContains(response, "Other User Note")  


class AuthTests(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("note_list"))
        self.assertEqual(response.status_code, 302)  # Redirect to login