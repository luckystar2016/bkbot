import time

from bilireq.dynamic import get_user_dynamics
import asyncio
from datetime import datetime, timedelta
import qqbot

from browser import get_dynamic_screenshot_mobile
from utils.dynamic import Dynamic
from sender import sender
from config import uids, last_time, live_ids

async def watcher():
    for uid, name in uids:
        if not uid or not name:
            return
        dynamics = (await get_user_dynamics(uid)).get("cards", [])

        if len(dynamics) == 0:
            return

        dynamic = dynamics[0]
        dynamic = Dynamic(**dynamic)
        if (
                dynamic.time > last_time[uid]
                and dynamic.time
                > datetime.now().timestamp() - timedelta(minutes=10).seconds
        ):
            last_time[uid] = dynamic.time
            qqbot.logger.info("pushing dy, uid: " + uid + " name: " + name)
            image = None
            for _ in range(3):
                try:
                    image = await get_dynamic_screenshot_mobile(dynamic.url)
                    dynamic.image = image
                    break
                except Exception:
                    pass
                await asyncio.sleep(0.1)
            if not image:
                pass
            await dynamic.format(image)
            await sender(dynamic)
        await asyncio.sleep(0.1)


if __name__ == '__main__':

    #loop = asyncio.get_event_loop()
    #result = loop.run_until_complete(watcher())
    #asyncio.run_coroutine_threadsafe(watcher(), loop)
    #schedule.every(10).seconds.do(asyncio.run_coroutine_threadsafe, (watcher(uids, guilds, bili_dy_pre, wait_time).start(), loop))
    #loop.close()
    time.sleep(100)