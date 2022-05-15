from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
import requests
from rest_framework_api_key.models import APIKey

from dates.models import DateFact
from dates.permissions import CheckApiKeyAuth
from dates.serializers import DateSerializer


@api_view(["GET","POST"])
def dates_fact_list(request: Request) -> Response:
    """
    This Function has two functionality
        1: Get all the dates_fact data in the database
        2: Post/Create/update date,and we get fact data using the date-fact-api(f"http://numbersapi.com/{month_number}/{day}/date"
           the client should deliver the day and month_number they want to update/create in the request body.
    :param request:
    :return: return the interesting fact of that specific day along with the day and month they provide.
    """
    if request.method == 'GET':
        date_fact = DateFact.objects.all()
        date_fact_serializer = DateSerializer(date_fact, many=True)
        return Response(date_fact_serializer.data, status.HTTP_200_OK)
    else:
        try:
            month_number = int(request.data['month'])
            day = int(request.data['day'])
        except KeyError as e:
            return Response(f"Key Error {e}", status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response(f"value Error {e}", status=status.HTTP_400_BAD_REQUEST)
        try:
            url = f"http://numbersapi.com/{month_number}/{day}/date"
            facts_response = requests.get(url)
            if facts_response.status_code == 200:
                fact = facts_response.text
            else:
                return Response(f"{facts_response.status_code, facts_response.text}",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.Timeout:
            return Response(f"request time out please try again", status=status.HTTP_408_REQUEST_TIMEOUT)
        except requests.exceptions.TooManyRedirects as e:
            return Response(f"{e}", status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.RequestException as e:
            return Response(f"{e}", status=status.HTTP_400_BAD_REQUEST)
        dates_fact = DateFact.objects.filter(month_number=month_number, day=day)
        if dates_fact.exists():
            dates_fact = dates_fact.last()
            dates_serializer = DateSerializer(dates_fact)
            dates_fact.days_checked = dates_fact.days_checked + 1
            dates_fact.save()
            return Response(dates_serializer.data, status=status.HTTP_201_CREATED)
        data = {"month_number": month_number, "day": day,"fact":fact}
        dates_serializer = DateSerializer(data=data)
        if not dates_serializer.is_valid():
            return Response(dates_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        dates_serializer.save()
        return Response(dates_serializer.data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes((CheckApiKeyAuth, ))
def date_fact_delete(request: Request, pk: int) -> Response:
    """
    The request should include the api_key of X-API-KEY with the <secret-key-value> in the header.
    :param request:
    :param pk: The id/primary key  for the data
    :return: The confirmation status code 204 if the delete request is successful
    """
    try:
        api_key_secret = request.META.get("HTTP_X_API_KEY")
        _ = APIKey.objects.get_from_key(api_key_secret)
        date_fact = DateFact.objects.get(id=pk)
        date_fact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except DateFact.DoesNotExist as e:
        return Response(f"{e}",status=status.HTTP_404_NOT_FOUND)
    except APIKey.DoesNotExist as e:
        return Response(f"Permission denied, {e}", status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET",])
def dates_fact_popular(request: Request) -> Response:
    """
    :param request:
    :return: The list of all dates_fact data by the descending order of number of checked date
    """
    date_facts = list(DateFact.objects.all().order_by('-days_checked'))
    payload = []
    for data_fact in date_facts:
        data = {}
        data["id"] = data_fact.id
        data["month"] = data_fact.get_month()
        data["days_checked"] = data_fact.days_checked
        payload.append(data)
    return Response(payload, status.HTTP_200_OK)