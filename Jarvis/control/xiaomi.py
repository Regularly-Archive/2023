from aiohttp import ClientSession
import asyncio
import logging
import json
import os
import sys
from pathlib import Path
from miservice import MiAccount, MiNAService, MiIOService, miio_command
from os import environ as env

class MiServiceController:

    def __init__(self):
        self.MI_USER = env.get('MI_USER')
        self.MI_PASS = env.get('MI_PASS')
        self.logger = logging.getLogger('MiServiceController')
        self.logger.setLevel(level=logging.DEBUG)

    async def execute_text_directive(self, text):
        try:
            async with ClientSession() as session:
                account = MiAccount(session, self.MI_USER, self.MI_PASS, os.path.join(str(Path.home()), '.mi.token'))
                service = MiNAService(account)
                devices = await service.device_list()
                device = list(filter(lambda x:x["name"] == "小爱同学", devices))[0]
                service = MiIOService(account)
                payload = { 
                    "did": device["miotDID"],
                    "siid": 7,
                    "aiid": 4,
                    "in":[ text, True ]
                }
                payload = json.dumps(payload)
                result = await miio_command(service, device["miotDID"], f"action {payload}")
                self.logger.info(f'通过小爱同学执行指令成功，返回值为: {json.dumps(result)}')
                return result
        except Exception as e:
            self.logger.error('通过小爱同学执行指令失败', exc_info=True)
            return None
            
class MiIOController:
    
    def __init__(self):
        self.MI_USER = env.get('MI_USER')
        self.MI_PASS = env.get('MI_PASS')
        self.logger = logging.getLogger('MiServiceController')
        self.logger.setLevel(level=logging.DEBUG)

    async def execute_text_directive(self, text):
         pass

async def main(text):
    controller = MiServiceController()
    result = await controller.execute_text_directive(text)
    print(result)

if __name__ == '__main__':
    # 方式1
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main('打开客厅灯'))
     
    # 方式2
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main('打开客厅灯'))