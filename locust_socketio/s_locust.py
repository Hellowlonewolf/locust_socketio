# -*-coding:UTF-8 -*-
from locust import HttpLocust, TaskSet, task, TaskSequence, Locust, events
import time, socketio, random


class SocketClient(object):

    def __init__(self, host):
        self.host = host
        self.ws = socketio.Client()
        self.connected = False

    def connect(self, burl):
        start_time = time.time()
		# 判断是否连接,连接就不执行
        if not self.connected:
            try:
                self.conn = self.ws.connect(url=burl)
                self.connected = True
            except Exception as e:
                total_time = int((time.time() - start_time) * 1000)

                events.request_failure.fire(request_type="socket", name='建立连接', response_time=total_time, exception=e)

            else:
                total_time = int((time.time() - start_time) * 1000)
                events.request_success.fire(request_type="socket", name='建立连接', response_time=total_time,
                                            response_length=0)

            return self.conn

    def emit(self, event, data, namespace):
        start_time = time.time()
        try:
            self.ws.emit(event, data, namespace)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)

            events.request_failure.fire(request_type="socket", name='加入/发送文本', response_time=total_time, exception=e)

        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="socket", name='加入/发送文本', response_time=total_time,
                                        response_length=0)

    def wait(self):
        return self.ws.wait()


class socketLocust(Locust):
    def __init__(self, *args, **kwargs):
        super(socketLocust, self).__init__(*args, **kwargs)
        self.client = SocketClient(self.host)


class SupperDianCan(TaskSet):
    @task
    def test(self):
        self.url = "https://xxx.com:6302"
        self.client.connect(self.url)
        #
        self.client.emit('join-room', {
            "user_id": 123,
            "team_id": 345
        }, namespace='/mz-chat')
        #
        self.client.emit('new_message', {
            "user_id": 123,
            "team_id": 345,
            "content": "我来了"}, namespace='/mz-chat')
        # period = int(time.strftime("%S", time.localtime())) + 9
        # while 1:
        #     nowtime = time.strftime("%S", time.localtime())
        #     self.s_sleep(5)
        #     self.client.emit('new_message', {
        #         "user_id": 123,
        #         "team_id": 345,
        #         "content": "data"}, namespace='/mz-chat')
        #     if int(nowtime) > period:
        #         break
        # self.wait()


class dc_socket(socketLocust):
    task_set = SupperDianCan
    min_wait = 1000
    max_wait = 2000


if __name__ == "__main__":
    import os

    os.system("locust -f s_locust1.py --no-web -c1 -r1 ")
