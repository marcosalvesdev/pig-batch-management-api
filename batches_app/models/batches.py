from django.db import models


class Batch(models.Model):
    STATUS_CHOICES = [
        ("created", "Created"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    batch_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="created")
    piglets_born = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Batch - {self.batch_id}"

    @property
    def name(self):
        return str(self)
