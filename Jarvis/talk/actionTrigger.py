import logging
class ActionTrigger:

    def __init__(self):
        self.routes = {}
        self.logger = logging.getLogger('ActionTrigger')
        self.logger.setLevel(logging.INFO)

    def route(self, keywords):
        def decorator(func):
            for keyword in keywords:
                self.routes[keyword] = func
            return func
        return decorator
    
    def execute(self, action):
        intent = action['intent']['name']
        query = action['query']
        if intent in self.routes:
            func = self.routes[intent]
            self.logger.debug(f"Executing trigger function '{func.__name__}' for intent '{intent}'")
            result = func(action)
            self.logger.debug(f"The result of trigger function '{func.__name__}' is '{result}'")
            return result
        elif query in self.routes:
            func = self.routes[query]
            self.logger.debug(f"Executing trigger function '{func.__name__}' for query '{intent}'")
            result = func(action)
            self.logger.debug(f"The result of trigger function '{func.__name__}' is '{result}'")
            return result
        else:
            self.logger.warning(f"No trigger function found for intent or query '{intent}'")
            return None
        
trigger = ActionTrigger()


