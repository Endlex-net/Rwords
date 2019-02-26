class IcibaInvalidWordException(Exception):
    """The word cannot be found in Iciba"""
    pass


class IcibaApiPasingException(Exception):
    """Iciba-API Information parsing exception."""
    pass


class WordRepeatAddException(Exception):
    """The word is already in the memory store."""
    pass


class LearnListEmptyException(Exception):
    """Today's learn list is empty"""
