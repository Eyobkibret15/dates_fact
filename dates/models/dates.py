import datetime

from django.core.exceptions import ValidationError
from django.db import models


def validate_month(value):
    if value in range(1, 13):
        return value
    else:
        raise ValidationError("This field accepts valid month only")


def validate_day(value):
    if value in range(1, 32):
        return value
    else:
        raise ValidationError("This field accepts valid day only")


class DateFact(models.Model):
    """
        Date fact model this will recorde the date fact along with number of days checked

        this will store the day and month number in integer format with a validation of real day and month number
        unfortunately I can't use DateField because
            1: SQL does not have an option to store only month and day without a year
            2: if I store using DateFact our logic will fail at 2/29 (lap year)
    """
    id = models.AutoField(primary_key=True)
    month_number = models.IntegerField(validators=[validate_month])
    day = models.IntegerField(validators=[validate_day])
    fact = models.TextField(verbose_name="Interesting Fact About the Date")
    days_checked = models.IntegerField(default=1)

    class Meta:
        unique_together = ('month_number', 'day',)
        verbose_name = "Date Event Fact"

    def get_month(self):
        month_number = str(self.month_number)
        datetime_object = datetime.datetime.strptime(month_number, "%m")
        month_name = datetime_object.strftime("%B")
        return month_name

    def __str__(self):
        month = self.get_month()
        day = str(self.day)
        return month + f" {day}"
