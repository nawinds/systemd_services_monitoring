import subprocess
from time import sleep
from datetime import datetime, timedelta
from modules.bot import bot
from modules.config import ADMIN_IDS, DB_PATH
from modules.data.db_session import create_session, global_init
from modules.data.services import Service
from os import system
from asyncio import get_event_loop


def check(service):
    result = subprocess.run(["sudo", "systemctl", "is-active", service])
    return_code = str(result.returncode)
    return return_code == "0"


async def notify(text):
    await bot.send_message(ADMIN_IDS[0], text)


async def send_logs(service):
    date = (datetime.now() - timedelta(minutes=15)).date()
    time = (datetime.now() - timedelta(minutes=15)).time()
    system(f'sudo journalctl --since "{date} {time}" -u {service} > temp/logs.txt')

    doc = open('temp/logs.txt', 'rb')
    await bot.send_document(ADMIN_IDS[0], document=doc)


async def down(service):
    text = f"{service} is 🔴 DOWN! Attempting to restart..."
    await notify(text)


async def restarted(service):
    text = f"{service} is 🔁🟢 RESTARTED successfully!"
    await notify(text)


async def broken(service):
    text = f"{service} is ⚠️ BROKEN! Restart attempts failed."
    await notify(text)


async def up(service):
    text = f"{service} is 🟢 UP!"
    await notify(text)


async def alert(service):
    with open("temp/alerted.txt", encoding="utf-8") as f:
        alerted = f.read().split("\n")
    if service in alerted:
        return
    await down(service)
    await send_logs(service)
    for i in range(3):
        subprocess.run(["sudo", "systemctl", "restart", service])
        sleep(5)
        if check(service):
            await restarted(service)
            return
    await broken(service)
    await send_logs(service)
    with open("temp/alerted.txt", "w", encoding="utf-8") as wf:
        wf.write("\n".join(alerted) + f"\n{service}")


if __name__ == "__main__":
    global_init(DB_PATH)
    session = create_session()
    all_services = session.query(Service).all()
    loop = get_event_loop()
    for s in all_services:
        is_up = check(s.name)

        if not is_up:
            loop.run_until_complete(alert(s.name))
        else:
            with open("temp/alerted.txt", encoding="utf-8") as f:
                alerted = f.read().split("\n")
            if s.name in alerted:
                alerted.remove(s.name)
                with open("temp/alerted.txt", "w", encoding="utf-8") as wf:
                    wf.write("\n".join(alerted))
                loop = get_event_loop()
                loop.run_until_complete(up(s.name))
    loop.close()
