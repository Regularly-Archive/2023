import sys

plugins = ['plugin1', 'plugin2', 'plugin3']
for plugin in plugins:
    __import__(plugin)
    sys.modules[plugin].run()