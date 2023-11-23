from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['full_name', 'CIN', 'debut_reservation', 'fin_reservation', 'num_tel', 'montant']
