import pytest
import json
from rest_framework_api_key.models import APIKey
from django.urls import reverse
from dates.apis.dates import dates_fact_list, date_fact_delete, dates_fact_popular
from rest_framework.test import APIRequestFactory

pytestmark = pytest.mark.django_db
factory = APIRequestFactory()


@pytest.mark.order(2)
def test_get_dates():
    """
        Test the Functionality of get all dates data api
    :return:
    """
    url = reverse("dates_fact_list")
    api = dates_fact_list
    response = api(factory.get(url))
    _ = response.render()
    assert response.status_code == 200
    assert response.content == b'[{"id":3,"month":"February","day":3,"fact":"days interesting fact"},{"id":4,"month":"May","day":7,"fact":"days 2 interesting fact"}]'


@pytest.mark.order(2)
def test_post_dates():
    """
        Test The Functionality of creation/update dates api
    :return:
    """
    url = reverse("dates_fact_list")
    api = dates_fact_list
    data = {
        "month": 6,
        "day": 7
    }
    response = api(factory.post(url, data=data))
    _ = response.render()
    content = json.loads(response.content)
    assert response.status_code == 201
    response_keys = ["id", "month", "day", "fact"]
    assert all(key in content.keys() for key in response_keys)
    assert content["month"] == "June"


@pytest.mark.order(3)
def test_delete_date():
    """
        Test The Functionality of  delete date api
    :return:
    """
    url_post = reverse("dates_fact_list")
    api_post = dates_fact_list
    data = {
        "month": 12,
        "day": 12
    }
    response_post = api_post(factory.post(url_post, data=data))
    _ = response_post.render()
    id = json.loads(response_post.content)["id"]

    api_key, key = APIKey.objects.create_key(name="X-API-KEY")
    header = {
        "HTTP_X_API_KEY" : "invalid_api-key",
    }

    url_delete = reverse("dates_fact_delete", args=(id,))
    api_delete = date_fact_delete

    request_no_key = factory.delete(url_delete,)
    response_no_key = api_delete(request_no_key,pk=id)
    assert response_no_key.status_code == 403

    request_invalid_key = factory.delete(url_delete, **header)
    response_no_key = api_delete(request_invalid_key,pk=id)
    assert response_no_key.status_code == 401

    header["HTTP_X_API_KEY"] = key
    request_valid = factory.delete(url_delete, **header)
    response_no_key = api_delete(request_valid, pk = id)
    assert response_no_key.status_code == 204


@pytest.mark.order(2)
def test_get_popular_dates():
    """
        Test The Functionality of get popular facts date in the descending order.
    :return:
    """
    url = reverse("dates_fact_popular")
    api = dates_fact_popular
    response = api(factory.get(url,))
    _ = response.render()
    content = json.loads(response.content)
    assert response.status_code == 200
    response_keys = ["id", "month", "days_checked"]
    assert all(key in content[0].keys() for key in response_keys)