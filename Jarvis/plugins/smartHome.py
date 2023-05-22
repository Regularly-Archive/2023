from talk.actionTrigger import trigger
from control.xiaomi import MiServiceController
from control.windows import shutdown, restart, calc, notepad
import sys, asyncio
sys.path.append('..')
from talk.actionTrigger import trigger

async def run(text):
    controller = MiServiceController()
    _ = await controller.execute_text_directive(text)


@trigger.route(keywords=['control_device','控制设备','控制家电','控制家居设备','控制家用设备','控制家居','打开设备'])
def control_device(action):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(action['query']))
    return '好的，主人，指令已下发。'
