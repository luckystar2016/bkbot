import asyncio
from datetime import datetime
from bilireq.dynamic import get_user_dynamics

guilds = []

uids = [
    ['672353429','贝拉'],
    ['672342685','乃琳'],
    ['672328094','嘉然'],
    ['672346917','向晚'],
    ['703007996','A-SOUL_Official'],
    ['2114847153','贝极星周报'],
]

live_ids = [

]

bili_dy_pre = 'https://t.bilibili.com/'
base_url = ''
wait_time = 10

dy_images_dir = "/home/images/"

last_time = dict()

now = datetime.now().timestamp()
for uid, name in uids:
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(get_user_dynamics(uid))
    dys = res.get("cards", [])
    latest_time = now
    if len(dys) > 0:
        latest_time = dys[0].get('desc').get('timestamp')
    last_time[uid] = latest_time