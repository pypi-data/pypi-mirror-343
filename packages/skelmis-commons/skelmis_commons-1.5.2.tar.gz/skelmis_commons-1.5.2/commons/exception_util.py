import traceback


def exception_as_string(error: Exception) -> str:
    """Given an exception, return the traceback as a string."""
    return "".join(traceback.format_exception(error))
