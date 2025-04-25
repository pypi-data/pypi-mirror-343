class ID10TException(Exception):
    suffix: str = "Please consult urban dictionary on what that means"
    message: str = "ID10T Exception occurred"
    
    """Base class for all ID10T exceptions."""
    def __init__(self, message="ID10T Exception occurred"):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message}. {self.suffix}'
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.message})'
    
    def __doc__(self):
        return f'{self.__class__.__name__} - {self.message}'

class ID10TError(ID10TException):
    pass

class ID10TWarning(Warning):
    suffix: str = "Please consult urban dictionary on what that means"
    message: str = "ID10T Warning occurred"
    
    """Base class for all ID10T warnings."""
    def __init__(self, message="ID10T Warning occurred"):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'{self.message}. {self.suffix}'
    
    def __repr__(self):
        return f'{self.__class__.__name__} ({self.message})'
    
    def __doc__(self):
        return f'{self.__class__.__name__} - {self.message}'