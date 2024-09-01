from batches_app.models import Batch
from django.db.models import Sum
from celery import shared_task
from django.core.cache import cache

from core.settings import IS_TESTING


REDIS_CACHE_KEY = "total_piglets_born"


def run(task, **kwargs):
    if IS_TESTING:
        task(**kwargs)
    else:
        task.delay(**kwargs)


@shared_task
def task_create_batch(data: dict):
    Batch.objects.create(**data)
    update_total_piglets_born(data["piglets_born"])


@shared_task
def task_update_batch(pk: str, data: dict):
    try:
        batch = Batch.objects.filter(id=pk)
        if not batch.exists():
            raise Batch.DoesNotExist
        current_batch_piglets_born = batch.first().piglets_born
        batch.update(**data)
        new_piglets_born = data["piglets_born"]
        if new_piglets_born:
            new_piglets_born, increase = calcute_update(
                current_batch_piglets_born, new_piglets_born
            )
            if new_piglets_born:
                update_total_piglets_born(new_piglets_born, increase)
    except Batch.DoesNotExist:
        return {"error": "Batch not found"}
    except Exception as e:
        return {"error": str(e)}


@shared_task
def task_delete_batch(pk: str):
    try:
        batch = Batch.objects.get(id=pk)
        batch_piglets_born = batch.piglets_born
        batch.delete()
        update_total_piglets_born(batch_piglets_born, increase=False)
    except Batch.DoesNotExist:
        return {"error": "Batch not found"}
    except Exception as e:
        return {"error": str(e)}


def get_total_piglets_born():
    total_piglets_born = cache.get(REDIS_CACHE_KEY)
    if not total_piglets_born or IS_TESTING:
        total_piglets_born = Batch.objects.aggregate(total=Sum("piglets_born")).get(
            "total"
        )
        cache.delete(REDIS_CACHE_KEY)
        cache.set(REDIS_CACHE_KEY, total_piglets_born, timeout=86400)
    return total_piglets_born


def update_total_piglets_born(piglets_born: int, increase: bool = True):
    total_piglets_born = get_total_piglets_born()
    if increase:
        new_total_piglets_born = total_piglets_born + piglets_born
    else:
        new_total_piglets_born = total_piglets_born - piglets_born
    cache.set(REDIS_CACHE_KEY, new_total_piglets_born, timeout=86400)


def calcute_update(current_batch_piglets_born, new_piglets_born: int):
    increase = True
    if current_batch_piglets_born == new_piglets_born:
        return None, None
    elif current_batch_piglets_born < new_piglets_born:
        diff = new_piglets_born - current_batch_piglets_born
    elif current_batch_piglets_born > new_piglets_born:
        diff = current_batch_piglets_born - new_piglets_born
        increase = False
    return diff, increase
