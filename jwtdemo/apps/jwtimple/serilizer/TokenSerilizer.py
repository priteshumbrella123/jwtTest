from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        is_active = 1 if user.is_active == True else 0
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['is_active'] = is_active
        return token
