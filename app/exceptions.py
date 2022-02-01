"""Custom Exception Classes"""


class ProjectException(Exception):
    """Base Exception for all exceptions in this application."""


class DataWriterException(ProjectException):
    """General Exception for Data Writers"""
