from django.test import TestCase
from rest_framework import status

from batches_app.models import Batch
from batches_app import tasks


class TestBatches(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.batch = Batch.objects.create(batch_id="1", piglets_born=10)
        cls.batch = Batch.objects.create(
            batch_id="2", piglets_born=10, status="in_progress"
        )

    def test_filter_by_status(self):
        response = self.client.get("/batches/?status=in_progress")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["batch_id"], "2")

    def test_create_batch(self):
        response = self.client.post("/batches/", {"batch_id": "3", "piglets_born": 10})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_batch = Batch.objects.get(batch_id="3")
        self.assertEqual(new_batch.batch_id, "3")

    def test_update_batch(self):
        response = self.client.put(
            f"/batches/{self.batch.id}/",
            {"piglets_born": 5},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.batch.refresh_from_db()
        updated_batch = Batch.objects.get(id=self.batch.id)
        self.assertEqual(updated_batch.piglets_born, 5)

    def test_delete_batch(self):
        response = self.client.delete(f"/batches/{self.batch.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_total_piglets_born_on_create(self):
        response = self.client.get("/batches/get_total_piglets_born/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["total_piglets_born"], 20)

    def test_caculate_pliglets_born_on_update(self):
        new_piglets_born, increase = tasks.calcute_update(5, 5)
        self.assertIsNone(new_piglets_born)
        self.assertIsNone(new_piglets_born)

        new_piglets_born, increase = tasks.calcute_update(5, 10)
        self.assertEqual(new_piglets_born, 5)
        self.assertTrue(increase)

        new_piglets_born, increase = tasks.calcute_update(10, 5)
        self.assertEqual(new_piglets_born, 5)
        self.assertFalse(increase)

        new_piglets_born, increase = tasks.calcute_update(0, 5)
        self.assertEqual(new_piglets_born, 5)
        self.assertTrue(increase)

        new_piglets_born, increase = tasks.calcute_update(5, 0)
        self.assertEqual(new_piglets_born, 5)
        self.assertFalse(increase)
