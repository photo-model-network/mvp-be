from rest_framework import serializers


class RequestReservationSerializer(serializers.Serializer):
    packageId = serializers.CharField(required=True)
    filmingDate = serializers.DateField(required=True)
    filmingStartTime = serializers.TimeField(required=True)
    selectedOption = serializers.IntegerField(required=True)


class PayReservationSerializer(serializers.Serializer):
    paymentId = serializers.CharField(required=True)
