from datetime import datetime
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from dates.models.dates import DateFact


class DateSerializer(ModelSerializer):
    """
    to Validate and retrieve dates from the DateFact Model
    """
    month = serializers.ReadOnlyField(source="get_month")

    class Meta:
        model = DateFact
        fields = ['id', 'month', 'month_number', 'day', 'fact', ]
        extra_kwargs = {
            'month_number': {'write_only': True},
        }

    def validate(self, data):
        month = data.get('month_number', None)
        day = data.get("day", None)
        date_check = f'2020/{month}/{day}'
        input_format = '%Y/%m/%d'
        try:
            _ = datetime.strptime(date_check, input_format)
            return data
        except ValueError as e:
            raise serializers.ValidationError(f"invalid date format {e}")
