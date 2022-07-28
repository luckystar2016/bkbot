from utils.dynamic import Dynamic

import asyncio
import os.path
import time

import qqbot
from qqbot.core.util.yaml_util import YamlUtil
from config import guilds, base_url

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))

async def sender(dynamic: Dynamic):
    t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
    msg_api = qqbot.AsyncMessageAPI(t_token, False)
    send = qqbot.MessageSendRequest(dynamic.message,'0', image=dynamic.image)
    for guild in guilds:
        try:
            await msg_api.post_message(guild, send)
            time.sleep(0.1)
        except Exception as e:
            qqbot.logger.error("guild: " + guild + "\tmessage: " + dynamic.message + " 发送失败")
            qqbot.logger.error(e)

async def pusu_test(guild):
    t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
    msg_api = qqbot.AsyncMessageAPI(t_token, False)
    #qqbot.logger.info("event_type %s" % dynamic.message + ",receive message %s" % message.content)
    for i in range(10):
        try:
            send = qqbot.MessageSendRequest("主动推送测试/n", '0', image= base_url + "687435805223813174.jpeg")
            await msg_api.post_message(guild, send)
        except Exception as e:
            print(e)
            time.sleep(1)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(pusu_test('8409342'))
    #qqbot_handler = qqbot.Handler(qqbot.HandlerType.AT_MESSAGE_EVENT_HANDLER, pusu_test)
    #qqbot.async_listen_events(t_token, True, qqbot_handler)
    loop.close()
