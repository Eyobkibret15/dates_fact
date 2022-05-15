from django.urls import path
from .dates import dates_fact_list,date_fact_delete,dates_fact_popular
urlpatterns = [
    path("dates/", dates_fact_list, name="dates_fact_list"),
    path("dates/<int:pk>/", date_fact_delete, name="dates_fact_delete"),
    path("popular/", dates_fact_popular, name="dates_fact_popular"),
]