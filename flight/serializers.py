from rest_framework import serializers

from .models import Flight, Passenger, Reservation


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            'id',
            'flightNumber',
            'operatingAirlines',
            'departureCity',
            'arrivalCity',
            'dateOfDeparture',
            'estimatedTimeOfDeparture'
        )


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = (
            'id',
            'firstName',
            'lastName',
            'email',
            'phoneNumber',
        )


class ReservationSerializer(serializers.ModelSerializer):

    passenger = PassengerSerializer(many=True, required=False)
    # ?-------------------------------------------
    #! flight id frontend'den seçilip gönderilecek bilgi
    flight = serializers.PrimaryKeyRelatedField(queryset=Flight.objects.all())
    #! ---------- OR ------------
    # flight_id = serializers.IntegerField(write_only=True)
    # ?-------------------------------------------
    # ?-------------------------------------------
    user = serializers.StringRelatedField()
    #! ---------- OR ------------
    user_id = serializers.IntegerField(write_only=True, required=False)
    # ?-------------------------------------------

    class Meta:
        model = Reservation
        fields = (
            'id',
            'user',
            'user_id',
            'passenger',
            'flight',
        )

    #! öncelikle passenger'ı hem passenger tablasuna hem de reservation tabloasuna create etmemiz gerekiyor.
    def create(self, validated_data):
        print(validated_data)
        #! validated data passenger içerisinde dönerek passenger verilerine ulaşmak istiyoruz. pop --> metodu ile istediğimiz key'i dictionary içerisiden alabiliyoruz.
        passenger_data = validated_data.pop('passenger')
        print(passenger_data)
        #! frontend'in göndermediği user'ı biz eklememiz gerekiyor.
        validated_data["user_id"] = self.context['request'].user.id
        #! user_id ve passenger verisine ulaşabildiğimiz için reservation create edebiliriz.
        reservation = Reservation.objects.create(**validated_data)
        #! reservation içerisine passenger'ları koyuyoruz
        for passenger in passenger_data:
            #! passenger'ı önce passenger tablosuna create edip id'yi alıyoruz. daha sonra reservation'a add yapıyoruz.
            reservation.passenger.add(Passenger.objects.create(**passenger))
            #! add --> metodu mantTomany den geliyor.
        reservation.save()

        return reservation


#! Staff user'lar için ayrı bir flight serializer oluşturuyoruz.
class StaffFlightSerializer(serializers.ModelSerializer):
    #! reservations --> ismini model içerisindeki related_name'den alıyoruz.
    reservations = ReservationSerializer(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = (
            'id',
            'flightNumber',
            'operatingAirlines',
            'departureCity',
            'arrivalCity',
            'dateOfDeparture',
            'estimatedTimeOfDeparture',
            'reservations'
        )
