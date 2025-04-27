class IncorrectDtype(Exception):
    def __init__(self,message):
        super().__init__(message)
    
class ModelNotFound(Exception):
    def __init__(self,message):
        super().__init__(message)
    