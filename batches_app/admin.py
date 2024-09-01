from django.contrib import admin

from batches_app.models import Batch


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "batch_id",
        "status",
        "piglets_born",
        "created_at",
        "updated_at",
    )
