import socketio, time
import asyncio
import coloredlogs
import logging

logging.getLogger().setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logging.getLogger().addHandler(console_handler)
coloredlogs.install(fmt='%(asctime)s,%(msecs)03d %(levelname)s %(filename)s:%(lineno)d %(message)s',
                    milliseconds=True, level='DEBUG')
# https://pypi.org/project/python-socketio/  文档
sio = socketio.AsyncClient()

tasks = []
@sio.event
def connect():
    print('connection established')


@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('new_message', {
        "user_id": 123,
        "team_id": 345,
        "content": "我来了"})


@sio.event
def disconnect():
    print('disconnected from server')


async def run_client():

    await sio.connect('https://xxxx.com:6302')
    await sio.sleep(5)
    print('my sid is', sio.sid)
    await sio.emit('join-room', {
        "user_id": 123,
        "team_id": 345
    }, namespace='/mz-chat')
    await sio.emit('new_message', {
        "user_id": 123,
        "team_id": 345,
        "content": "星期五"

    }, namespace='/mz-chat')


def run():
    for i in range(1):
        task = asyncio.ensure_future(run_client())
        tasks.append(task)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.run_forever()
    loop.close()