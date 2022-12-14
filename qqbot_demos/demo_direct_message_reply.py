#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

import qqbot
from qqbot.core.util.yaml_util import YamlUtil
from qqbot.model.ws_context import WsContext

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))


async def _direct_message_handler(context: WsContext, message: qqbot.Message):
    """
    定义事件回调的处理

    :param context: WsContext 对象，包含 event_type 和 event_id
    :param message: 事件对象（如监听消息是Message对象）
    """
    msg_api = qqbot.AsyncDmsAPI(t_token, False)
    # 打印返回信息
    qqbot.logger.info("event_type %s" % context.event_type + ",receive message %s" % message.content)
    # 构造消息发送请求数据对象
    send = qqbot.MessageSendRequest("收到你的私信消息了：%s" % message.content, message.id)
    # 通过api发送回复消息
    await msg_api.post_direct_message(message.guild_id, send)


if __name__ == "__main__":
    t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
    qqbot_handler = qqbot.Handler(qqbot.HandlerType.DIRECT_MESSAGE_EVENT_HANDLER, _direct_message_handler)
    qqbot.async_listen_events(t_token, False, qqbot_handler)
