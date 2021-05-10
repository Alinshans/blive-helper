import asyncio
import threading
import requests

from blive.bliveclient import BLiveClient


class BLiveThread(threading.Thread):
    def __init__(self, room_id=0):
        threading.Thread.__init__(self, daemon=True)
        self.room_id = room_id
        self.client = None
        self.event = threading.Event()

    def run(self):
        print('blivethread run')
        while True:
            self.event.wait()
            asyncio.run(self.blive_connect())
            self.event.clear()

    def set_room_id(self, room_id):
        self.room_id = room_id
        self.event.set()

    async def blive_connect(self):
        print(f'blivethread connect room_id={self.room_id}')
        self.client = BLiveClient(self.room_id, ssl=True)
        future = self.client.start()
        try:
            await future
        finally:
            if self.client:
                await self.client.close()
                self.client = None
                print('finally')

    def connect_room(self, room_id):
        r = requests.get(f'http://api.live.bilibili.com/room/v1/Room/room_init?id={room_id}')
        json = r.json()
        # 房间不存在
        if json["code"] == 60004:
            return False
        self.room_id = room_id
        self.event.set()
        return True

    def disconnect_room(self):
        if self.client:
                print('blivethread disconnect')
                self.client.stop()
