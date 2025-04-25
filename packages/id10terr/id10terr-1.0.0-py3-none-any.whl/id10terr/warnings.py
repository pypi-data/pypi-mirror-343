from .interface import ID10TWarning

class DidntReadDocsWarning(ID10TWarning):
    suffix: str = "Please refer to the documentation for more information."
    message: str = "Did you read the documentation?"
    """Warning raised when a user doesn't read the documentation."""

    def __init__(self, message="Did you read the documentation?"):
        self.message = message
        super().__init__(self.message)

class DidntUseBrainWarning(ID10TWarning):
    suffix: str = "Please refer to your inner computer for more information (\"the brain\")."
    message: str = "Did you use your brain?"
    """Warning raised when a user doesn't use their brain."""
    def __init__(self, message="Did you use your brain?"):
        self.message = message
        super().__init__(self.message)
        
class BrainFartWarning(ID10TWarning):
    suffix: str = "Please refer to your inner computer for more information (\"the brain\")."
    message: str = "Did you have a brain fart?"
    """Warning raised when a user has a brain fart."""
    def __init__(self, message="Did you have a brain fart?"):
        self.message = message
        super().__init__(self.message)

class WasntVerySmartWarning(ID10TWarning):
    suffix: str = "Please re-think your life choices"
    message: str = "That wasn't very smart, was it?"
    
    """Warning raised when a choice made by the user isn't very smart."""
    def __init__(self, message="That wasn't very smart, was it?"):
        self.message = message
        super().__init__(self.message)