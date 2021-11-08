from db.repositories.prop import PropRepository

from consumer.base import BaseConsumer
from consumer.callbacks import on_prop_msg



async def start_props_consumer(app):
    db = app.state._db()
    try:
        await app.state._consumer.start_consuming(
            PropRepository(db),
            exchange='props',
            binding_key='prop.*',
            cb=on_prop_msg,
            queue='prop_changes')
    finally:
        db.close()

async def init_consumers(app):
    app.state._consumer = BaseConsumer(broker_conn=app.state._broker_conn)
    await start_props_consumer(app)