from .interface import ID10TException

class DidntReadDocsException(ID10TException):
    suffix: str = "Please refer to the documentation for more information."
    message: str = "Did you read the documentation?"
    """Exception raised when a user doesn't read the documentation."""

    def __init__(self, message="Did you read the documentation?"):
        self.message = message
        super().__init__(self.message)

class DidntReadDocsError(DidntReadDocsException):
    pass

class DidntUseBrainException(ID10TException):
    suffix: str = "Please refer to your inner computer for more information (\"the brain\")."
    message: str = "Did you use your brain?"
    """Exception raised when a user doesn't use their brain."""
    def __init__(self, message="Did you use your brain?"):
        self.message = message
        super().__init__(self.message)

class DidntUseBrainError(DidntUseBrainException):
    pass

class BrainFartException(ID10TException):
    suffix: str = "Please refer to your inner computer for more information (\"the brain\")."
    message: str = "Did you have a brain fart?"
    """Exception raised when a user has a brain fart."""
    def __init__(self, message="Did you have a brain fart?"):
        self.message = message
        super().__init__(self.message)

class BrainFartError(BrainFartException):
    pass

class WasntVerySmartException(ID10TException):
    suffix: str = "Please re-think your life choices"
    message: str = "That wasn't very smart, was it?"
    
    """Exception raised when a choice made by the user isn't very smart."""
    def __init__(self, message="That wasn't very smart, was it?"):
        self.message = message
        super().__init__(self.message)

class WasntVerySmartError(WasntVerySmartException):
    pass