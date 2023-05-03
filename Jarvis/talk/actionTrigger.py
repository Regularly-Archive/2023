import logging
class ActionTrigger:

    def __init__(self):
        self.routes = {}
        self.logger = logging.getLogger('ActionTrigger')
        self.logger.setLevel(logging.INFO)

    def route(self, keywords):
        def decorator(func):
            for keyword in keywords:
                if keyword in self.routes:
                    self.routes[keyword].append(func)
                else:
                    self.routes[keyword] = [func]
            return func
        return decorator
    
    def execute(self, action):
        if action == None:
            return None
        intent = action['intent']['name']
        query = action['query']
        if intent in self.routes:
            funcs = self.routes[intent]
            for func in funcs:
                self.logger.debug(f"Executing trigger function '{func.__name__}' for intent '{intent}'")
                result = func(action)
                self.logger.debug(f"The result of trigger function '{func.__name__}' is '{result}'")
                if result != None:
                    return result
        elif query in self.routes:
            funcs = self.routes[query]
            for func in funcs:
                self.logger.debug(f"Executing trigger function '{func.__name__}' for intent '{intent}'")
                result = func(action)
                self.logger.debug(f"The result of trigger function '{func.__name__}' is '{result}'")
                if result != None:
                    return result
        else:
            self.logger.warning(f"No trigger function found for intent or query '{intent}'")
            return None
        
trigger = ActionTrigger()


