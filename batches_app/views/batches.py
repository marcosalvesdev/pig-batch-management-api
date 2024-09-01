from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from batches_app import tasks
from batches_app.models.batches import Batch
from batches_app.serializers.batches import BaseBatchSerializer


class BatchesViewSet(ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BaseBatchSerializer
    filterset_fields = ["status"]

    @action(detail=False, methods=["get"])
    def get_total_piglets_born(self, request, *args, **kwargs):
        total_piglets_born = tasks.get_total_piglets_born()

        return Response({"total_piglets_born": total_piglets_born or 0})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        tasks.run(tasks.task_create_batch, data=validated_data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance=instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        tasks.run(tasks.task_update_batch, pk=instance.id, data=validated_data)

        return Response(validated_data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        tasks.run(tasks.task_delete_batch, pk=kwargs.get("pk"))

        return Response(status=status.HTTP_204_NO_CONTENT)
