import asyncio
import traceback
from datetime import datetime, timedelta

from bilireq.dynamic import get_user_dynamics
from browser import get_dynamic_screenshot_mobile
import asyncio

async def dy_sched():
    """直播推送"""
    uid = "672353429"
    name = "贝拉"
    dy_url_pre = "https://t.bilibili.com/"
    if not uid:
        return

    # 获取最近十二条动态
    dynamics = (await get_user_dynamics(uid)).get("cards", [])
    # config['uid'][uid]['name'] = dynamics[0]['desc']['user_profile']['info']['uname']
    # await update_config(config)

    if len(dynamics) == 0:  # 没有发过动态或者动态全删的直接结束
        return

    dynamic = None
    for dynamic in dynamics[::-1]:  # 从旧到新取最近5条动态
            url = dy_url_pre + str(dynamic['desc']['dynamic_id'])
            #url = "https://xingzheai.cn/"
            image = None
            for _ in range(3):
                image = await get_dynamic_screenshot_mobile(url)
                break

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(dy_sched())
    loop.close()