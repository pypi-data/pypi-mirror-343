"""OroaTLO CLI - A command-line interface for TLO searches"""

from .api import TLOApi, TLOApiError

__version__ = "0.1.0"

# Make main classes available at package level
__all__ = ['TLOApi', 'TLOApiError', 'search', 'format_results']

def search(admin_key: str, **params):
    """
    Quick search function that can be used without creating a TLOApi instance
    """
    api = TLOApi(admin_key)
    return api.search(**params)

def format_results(data):
    """
    Format search results without needing to create a TLOApi instance
    """
    api = TLOApi("")  # Empty key since it's not needed for formatting
    return api.format_person_data(data) 