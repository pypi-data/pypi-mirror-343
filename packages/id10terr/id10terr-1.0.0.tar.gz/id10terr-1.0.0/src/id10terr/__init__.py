from .interface import ID10TError, ID10TException, ID10TWarning
from .errors import DidntReadDocsError, DidntReadDocsException, DidntUseBrainError, DidntUseBrainException, WasntVerySmartError, WasntVerySmartException, BrainFartError, BrainFartException
from .warnings import DidntReadDocsWarning, DidntUseBrainWarning, WasntVerySmartWarning, BrainFartWarning

# Add to __all__ for public API
__all__ = [
    "ID10TError",
    "ID10TException",
    "ID10TWarning",
    "DidntReadDocsError",
    "DidntReadDocsException",
    "DidntUseBrainError",
    "DidntUseBrainException",
    "WasntVerySmartError",
    "WasntVerySmartException",
    "BrainFartError",
    "BrainFartException",
    "DidntReadDocsWarning",
    "DidntUseBrainWarning",
    "WasntVerySmartWarning",
    "BrainFartWarning",
]
    