#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import os.path

import qqbot
from qqbot.model.ws_context import WsContext

async def _message_handler(context: WsContext, message: qqbot.Message):
    """
    定义事件回调的处理

    :param context: WsContext 对象，包含 event_type 和 event_id
    :param message: 事件对象（如监听消息是Message对象）
    """
    msg_api = qqbot.AsyncMessageAPI(t_token, False)
    # 打印返回信息

    if '/sub' in message.content:
        #+ "guild %s" % message.guild_id + "subcribe %s" %
        print(message.channel_id, message.guild_id)
        guilds.append(message.guild_id)
        send = qqbot.MessageSendRequest("订阅成功")
        await msg_api.post_message(message.channel_id, send)

        '''
            print(message.channel_id, message.guild_id)
            send = qqbot.MessageSendRequest("你好，贝极星", message.id)
            await msg_api.post_message(message.channel_id, send)
        '''