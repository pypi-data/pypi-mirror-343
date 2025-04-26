"""
Custom exceptions for the TriaHRDataGatherer library.
"""

class TriaHRDataGathererError(Exception):
    """Base class for all TriaHRDataGatherer exceptions."""
    pass

class UserNotFoundError(TriaHRDataGathererError):
    """Raised when a user cannot be found by email or ID."""
    pass

class DataFetchError(TriaHRDataGathererError):
    """Raised when there is an error fetching data from the API."""
    pass