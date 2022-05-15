import pytest
from django.utils import timezone
from dates.models import DateFact
pytestmark = pytest.mark.django_db(transaction=True)

"""
fixtures for all test database setup  they can access it by default from this file 
"""


@pytest.fixture(autouse=True)
def set_up_dates_model() -> dict:
    """
    this fixture will create the first setup for DateFact models
    :return: a python dictionary that we can access it from test_models using keys
    """
    #  why    dim

    date = DateFact.objects.create(month_number=2, day=3,
                                    fact="days interesting fact")
    date2 = DateFact.objects.create(month_number=5, day=7,
                                   fact="days 2 interesting fact")
    initial = {
        "date": date,
    }

    return initial