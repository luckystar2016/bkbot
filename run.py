from utils.dynamic import Dynamic
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
import qqbot
from qqbot.core.util.yaml_util import YamlUtil
from qqbot.model.ws_context import WsContext
from watcher import watcher

from config import guilds, wait_time


test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))
t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])

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
        if message.channel_id not in guilds:
            guilds.append(message.channel_id)
        send = qqbot.MessageSendRequest("订阅成功", message.id)
        await msg_api.post_message(message.channel_id, send)

    if 'hi' in message.content:
        print(message.channel_id, message.guild_id)
        send = qqbot.MessageSendRequest("<@%s>你好, 贝极星" % message.author.username, message.id)
        await msg_api.post_message(message.channel_id, send)

async def sender(dynamic: Dynamic):
    t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
    msg_api = qqbot.AsyncMessageAPI(t_token, False)
    #qqbot.logger.info("event_type %s" % dynamic.message + ",receive message %s" % message.content)
    send = qqbot.MessageSendRequest(dynamic.message, '0', image=dynamic.image)
    for guild in guilds:
        await msg_api.post_message(guild, send)

if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    job = scheduler.add_job(watcher, 'interval', seconds=wait_time)
    scheduler.start()

    qqbot_handler = qqbot.Handler(qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, _message_handler)
    qqbot.async_listen_events(t_token, False, qqbot_handler)