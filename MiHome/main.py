from aiohttp import ClientSession
import asyncio
import logging
import json
import os
import sys
from pathlib import Path
from miservice import MiAccount, MiNAService, MiIOService, miio_command

MI_USER = os.environ.get('MI_USER') or ""
MI_PASS = os.environ.get('MI_PASS') or ""

async def main(args):
    try:
        async with ClientSession() as session:
            account = MiAccount(session, MI_USER, MI_PASS, os.path.join(str(Path.home()), '.mi.token'))
            service = MiNAService(account)
            devices = await service.device_list()
            device = list(filter(lambda x:x["name"] == "小爱同学", devices))[0]

            service = MiIOService(account)
            result = await miio_command(service, device["miotDID"], "7-3 Hello")
    except Exception as e:
        result = e
        print(result)

if __name__ == "__main__":
    argv = sys.argv
    asyncio.run(main(argv))