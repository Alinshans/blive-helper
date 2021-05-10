import thirdparty.blivedm as blivedm


class BLiveClient(blivedm.BLiveClient):
    _COMMAND_HANDLERS = blivedm.BLiveClient._COMMAND_HANDLERS.copy()

    async def __on_vip_enter(self, command):
        print(command)

    _COMMAND_HANDLERS['WELCOME'] = __on_vip_enter  # 老爷入场

    async def _on_receive_popularity(self, popularity: int):
        print(f'当前人气值：{popularity}')

    async def _on_receive_danmaku(self, danmaku: blivedm.DanmakuMessage):
        print(f'{danmaku.uname}：{danmaku.msg}')

    async def _on_receive_gift(self, gift: blivedm.GiftMessage):
        print(f'{gift.uname} 赠送{gift.gift_name}x{gift.num} （{gift.coin_type}币x{gift.total_coin}）')

    async def _on_buy_guard(self, message: blivedm.GuardBuyMessage):
        print(f'{message.username} 购买{message.gift_name}')

    async def _on_super_chat(self, message: blivedm.SuperChatMessage):
        print(f'醒目留言 ¥{message.price} {message.uname}：{message.message}')



