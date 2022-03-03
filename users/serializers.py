from dj_rest_auth.serializers import TokenSerializer
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, validators


class RegisterSerializer(serializers.ModelSerializer):

    #! kullanıcın zorunlu oalrak email girmesini istiyoruz.
    email = serializers.EmailField(required=True, validators=[
                                   validators.UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
        #! style={'input_type': 'password'} -> password'u ***** olarak göstermek için
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name",
                  "email", "password", "password2"]
        extra_kwargs = {
            #! response olarak bunları dönmüyoruz. write_only=True --> yukarıda da tanımlayabiliyoruz.
            'password': {'write_only': True},
            'password2': {'write_only': True},
        }

    def create(self, validated_data):
        #! validated_dta frontend'den gelen veriler
        password = validated_data.get("password")
        #! frontend passwor2'yi de gönderiyor ancak backend'de User create ederken User modelimizde password2 olmadığı için password2'yi çıkartmamız gerekiyor. o yüzden passwor2'yi pop metodu ile dict içerisinden çıkarıyorruz.
        validated_data.pop("password2")
        user = User.objects.create(**validated_data)
        #! password'i hashleyip kaydediyoruz.
        user.set_password(password)
        user.save()
        return user

    #! diğer validation'lar için dokümantasyonda serializer içerisindeki validation kısmını incele
    def validate(self, data):
      #! object-level validation
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return data


#! Loginde token ile kullanıcı bilgilerini almak için
class UserTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")

#! Login yaptığımız zaman token ile diğer user bilgilerini de göndermek istiyoruz.


class CustomTokenSerializer(TokenSerializer):

    #! Django yukarıdan aşağıya çalıştığı için UserTokenSerializer'ı yukarıda tanımlıyoruz.
    user = UserTokenSerializer(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = ("key", "user")
        #! key --> token
        #! user'ın bilgilerini göndermek için user field'ını ekliyoruz.
