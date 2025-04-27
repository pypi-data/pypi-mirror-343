class ShadowScriptError(Exception):
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details
        super().__init__(f"{error_name}: {details}")

class SyntaxError(ShadowScriptError):
    def __init__(self, details):
        super().__init__("SyntaxError", details)

class RuntimeError(ShadowScriptError):
    def __init__(self, details):
        super().__init__("RuntimeError", details)

class NameError(ShadowScriptError):
    def __init__(self, details):
        super().__init__("NameError", details)

class TypeError(ShadowScriptError):
    def __init__(self, details):
        super().__init__("TypeError", details)