from rest_framework import serializers


from batches_app.models import Batch


class BaseBatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Batch
        fields = "__all__"
        readlonly_fields = ("created_at", "updated_at")
