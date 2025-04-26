import datetime


def get_current_utc() -> datetime.datetime:
    """Fetch a UTC timezone aware datetime.

    Returns
    -------
    datetime.datetime
        The current UTC time as an aware datetime.
    """
    return datetime.datetime.now(tz=datetime.timezone.utc)


def is_within_next_(
    current_datetime: datetime.datetime,
    expected_datetime: datetime.datetime,
    delta: datetime.timedelta = datetime.timedelta(minutes=5),
) -> bool:
    """Returns true if the times are within X minutes of each other

    Parameters
    ----------
    current_datetime : datetime.datetime
        Now.
    expected_datetime : datetime.datetime
        When you want the thing to occur.
    delta : datetime.timedelta
        Return true if the two datetimes are within this delta.

        Defaults to 5 minutes.

    Returns
    -------
    bool
        True if times within the given delta.
    """
    if is_in_the_past(current_datetime, expected_datetime):
        # Date is in the past
        return False

    difference = expected_datetime - current_datetime
    if difference < delta:
        return True

    return False


def is_in_the_past(
    current_datetime: datetime.datetime,
    expected_datetime: datetime.datetime,
) -> bool:
    """Returns True if the datetime is in the past."""
    return current_datetime > expected_datetime
