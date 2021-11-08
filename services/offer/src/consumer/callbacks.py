from aio_pika import IncomingMessage

from db.repositories.prop import PropRepository
import schemas


async def on_prop_msg(repo: PropRepository, msg: IncomingMessage):
    msg_type = msg.routing_key.split('.')[1]

    print('## prop msg rec', msg.body)

    if msg_type == 'add':
        new_prop = schemas.PropCreate.parse_raw(msg.body)
        await repo.create(prop=new_prop)
        msg.ack()

    if msg_type == 'update':
        update_prop = schemas.PropUpdate.parse_raw(msg.body)
        await repo.update(prop=update_prop)
        msg.ack()