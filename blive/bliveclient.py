import thirdparty.blivedm.blivedm as blivedm


class BLiveClient(blivedm.BLiveClient):
    _COMMAND_HANDLERS = blivedm.BLiveClient._COMMAND_HANDLERS.copy()

    async def __on_vip_enter(self, command):
        self.signal.emit(command)
        print(command)

    _COMMAND_HANDLERS['WELCOME'] = __on_vip_enter  # 老爷入场

    async def _on_live(self, message):
        print(message)
        self.signal.emit('live')

    async def _on_preparing(self, message):
        print(message)
        # 有 round 字段时是轮播
        if message.__contains__('round'):
            self.signal.emit('round')
        else:
            self.signal.emit('preparing')

    async def _on_receive_popularity(self, popularity: int):
        self.signal.emit(popularity)
        print(f'当前人气值：{popularity}')

    async def _on_receive_danmaku(self, danmaku: blivedm.DanmakuMessage):
        self.signal.emit(danmaku)
        print(f'{danmaku.uname}：{danmaku.msg}')

    async def _on_receive_gift(self, gift: blivedm.GiftMessage):
        print(f'{gift.uname} 赠送{gift.gift_name}x{gift.num} （{gift.coin_type}币x{gift.total_coin}）')

    async def _on_buy_guard(self, message: blivedm.GuardBuyMessage):
        print(f'{message.username} 购买{message.gift_name}')

    async def _on_super_chat(self, message: blivedm.SuperChatMessage):
        print(f'醒目留言 ¥{message.price} {message.uname}：{message.message}')
