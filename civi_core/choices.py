"""
## Description
Static choices.
"""
import enum


class Party(enum.Enum):
    UNKNOWN = 'unknown'
    independent = 'independent'
    democratic = 'democratic'
    republic = 'republic'
