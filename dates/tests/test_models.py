import pytest
from django.utils import timezone
from dates.models import DateFact

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.mark.order(1)
def test_date_fact_model(set_up_dates_model):
    """
    this test function will test the behaviour of DateFact  model
    """
    initial_date = set_up_dates_model["date"]
    date = DateFact.objects.get(month_number=2, day=3,
                                fact="days interesting fact")
    assert date.month_number == initial_date.month_number
    assert date.day == initial_date.day
    assert date.fact == initial_date.fact
    assert date.get_month() == "February"
    assert date.days_checked == 1
