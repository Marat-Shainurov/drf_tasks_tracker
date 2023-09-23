from datetime import datetime, timedelta

import pytz
from rest_framework.exceptions import ValidationError


class IsDeadlineOk:
    """
    arg: field name.
    returns: bool
    Checks whether the set deadline value is valid or not.
    The set deadline can't be earlier than 8 hours from the current time.
    """
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        deadline = dict(value).get(self.field)
        now = datetime.now(pytz.UTC)
        delta = now - deadline
        deadline_limit = timedelta(hours=8)
        if delta > deadline_limit:
            raise ValidationError("The 'deadline' value can't be earlier than 8 hours from the current time")
