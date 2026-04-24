from celery import Celery

celery_app = Celery("platform_worker", broker="redis://redis:6379/0", backend="redis://redis:6379/1")


@celery_app.task
def heartbeat() -> str:
    return "worker-ok"
