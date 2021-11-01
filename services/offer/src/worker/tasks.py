from worker.celery import app



@app.task
def add(x: int, y: int) -> int:
    return x + y