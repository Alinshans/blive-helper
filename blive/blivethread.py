import asyncio
import threading
import requests

from PyQt5.QtCore import QThread, pyqtSignal
from blive.bliveclient import BLiveClient


class RoomInfo(object):
    def __init__(self, room_id=0, uid=0, status=0, title=None, popularity=0, up_name=None, up_avatar=None):
        self.room_id = room_id
        self.uid = uid
        self.status = status
        self.title = title
        self.popularity = popularity
        self.up_name = up_name
        self.up_avatar = up_avatar


class BLiveThread(QThread):
    on_message = pyqtSignal(object)
    live_status = ['未开播', '直播中', '轮播中']

    def __init__(self, room_id=0):
        QThread.__init__(self)
        self.room_id = room_id
        self.client = None
        self.event = threading.Event()
        self.room_info = RoomInfo()

    def run(self):
        print('blivethread start')
        while True:
            self.event.wait()
            asyncio.run(self.blive_connect())
            self.event.clear()

    async def blive_connect(self):
        print(f'blivethread connect room_id={self.room_id}')
        self.client = BLiveClient(self.room_id, self.on_message, ssl=True)
        future = self.client.start()
        try:
            await future
        finally:
            if self.client:
                await self.client.close()
                self.client = None

    def connect_room(self, room_id):
        r = requests.get(f'https://api.live.bilibili.com/room/v1/Room/get_info?room_id={room_id}')
        json = r.json()
        # 房间不存在
        if json['code'] == 1:
            return None
        self.room_info.room_id = room_id
        self.room_info.uid = json['data']['uid']
        self.room_info.status = self.live_status[int(json['data']['live_status'])]
        self.room_info.title = json['data']['title']
        self.room_info.popularity = json['data']['online']
        r = requests.get('https://api.bilibili.com/x/space/acc/info?mid={}'.format(self.room_info.uid))
        json = r.json()
        if json['code'] == 0:
            self.room_info.up_name = json['data']['name']
            self.room_info.up_avatar = json['data']['face']
        self.room_id = room_id
        self.event.set()
        return self.room_info

    def disconnect_room(self):
        if self.client:
            print('blivethread disconnect')
            self.client.stop()
