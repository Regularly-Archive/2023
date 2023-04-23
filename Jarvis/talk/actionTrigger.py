import logging
class ActionTrigger:

    def __init__(self):
        self.routes = {}
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def route(self, keywords):
        def decorator(func):
            for keyword in keywords:
                self.routes[keyword] = func
            return func
        return decorator
    
    def execute(self, action):
        intent = action['intent']['name']
        if intent in self.routes:
            func = self.routes[intent]
            self.logger.debug(f"Executing trigger function '{func.__name__}' for intent '{intent}'")
            result = self.routes[intent](action)
            self.logger.debug(f"The result of trigger function '{func.__name__}' is '{result}'")
            return result
        else:
            self.logger.warning(f"No trigger function {func.__name__} found for intent '{intent}'")
            return None
        
trigger = ActionTrigger()


