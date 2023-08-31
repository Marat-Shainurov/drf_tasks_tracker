from datetime import datetime, timedelta

from rest_framework.exceptions import ValidationError


class IsDeadlineOk:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        deadline = dict(value).get(self.field)
        now = datetime.now()
        delta = now - deadline.replace(tzinfo=None)
        deadline_limit = timedelta(hours=8)
        if delta > deadline_limit:
            raise ValidationError(f"The 'deadline' value can't be earlier than 8 hours from the current time")
