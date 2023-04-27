from talk.actionTrigger import trigger
from control.xiaomi import MiServiceController
from control.windows import shutdown, restart, calc, notepad
import sys, asyncio
sys.path.append('..')
from talk.actionTrigger import trigger

async def run(text):
    controller = MiServiceController()
    result = await controller.execute_text_directive(text)
    return '指令已下发'

@trigger.route(keywords=['控制设备','控制'])
def control_device(action):
    controller = MiServiceController()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(action['query']))

@trigger.route(keywords=['关闭计算机'])
def shutdown_computer(action):
    shutdown()
    return '已执行关机指令'

@trigger.route(keywords=['重启计算机'])
def restart_computer(action):
    restart()
    return '已执行重启指令'

@trigger.route(keywords=['打开应用', '打开记事本'])
def open_notepad(action):
    notepad()
    return '已打开记事本'

@trigger.route(keywords=['打开应用', '打开计算器'])
def open_calc(action):
    calc()
    return '已打开计算器'