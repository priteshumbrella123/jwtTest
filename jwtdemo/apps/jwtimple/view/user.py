from rest_framework.views import APIView
from rest_framework.response import Response
from apps.jwtimple.serilizer.RegistrationSerializer import UserCreateSerializer,UserListSerializer,UserUpdateSerializer
from rest_framework import status as http_status_codes
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from apps.jwtimple.helper import jwt_helper
from apps.jwtimple.helper.jwt_helper import jwt_check
from django.utils import timezone
from apps.jwtimple.helper import permission
from django.contrib.auth import logout


class Userlogin(APIView):

    User = get_user_model()

    def post(self, request):
        if not request.data:
            return Response({'Error': "Please provide username/password"}, status="400")
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if username and password:
            try:
                #x = self.User.objects.all()
                user = authenticate(username=username, password=password)
                if user.is_active:
                    user.last_login = timezone.now()
                    user.save()
                    user_detail = {'username': user.username, 'password': password}
                    return Response({'message': 'You have been successfully logged in',
                                     'data': jwt_helper.get_my_token(user_detail)},
                                     status=http_status_codes.HTTP_200_OK)
            except Exception as e:
                return Response({'error': 'Invalid Credential'}, status= http_status_codes.HTTP_401_UNAUTHORIZED)

import json
class Userlogout(APIView):

    def post(self, request):
        print(request.META['AU'])
        #logout(request)
        return Response({'message': 'You have been successfully logged out', 'data': {}},
                        status=http_status_codes.HTTP_200_OK)


class UserRegistration(APIView):
    User = get_user_model()
    def post(self,request):
        data = request.data
        serilizer = UserCreateSerializer(data=data)
        if serilizer.is_valid():
            serilizer.save()
            return Response({'message': "{} is successfully created.".format("User"), 'data': {}},
                            status=http_status_codes.HTTP_201_CREATED)
        tmp_errors = {key: serilizer.errors[key][0] for key in serilizer.errors}
        return Response({'message': "Invalid data", 'error': tmp_errors, 'data': {}},
                        status=http_status_codes.HTTP_400_BAD_REQUEST)

    @jwt_check(module_action_list= [permission.user_list])
    def get(self,request):
        user = self.User.objects.filter(is_active = True,is_deleted = False).order_by('-id')
        serializer = UserListSerializer(user, many=True)
        return Response(
            {'message': "{} list".format("User"), 'data': serializer.data}, status=http_status_codes.HTTP_200_OK)


class UserDetailApi(APIView):

    User = get_user_model()

    def get_object(self, id):
        try:
            return self.User.objects.get(id=id)
        except self.User.DoesNotExist as e:
            return False

    @jwt_check(module_action_list=[permission.user_detail])
    def get(self, request, id=None):
        instance = self.get_object(id)
        if not instance:
            return Response({'message': "not found".format("user"), 'data': {}},
                            status=http_status_codes.HTTP_404_NOT_FOUND)

        if request.user.id == int(id):
            serializer = UserListSerializer(instance)
        else:
            return Response({'message': 'you can view only your detail', 'data':{}})

        return Response({'message': 'get user', 'data': serializer.data}, status=http_status_codes.HTTP_200_OK)

    @jwt_check(module_action_list=[permission.user_update])
    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        if not instance:
            return Response({'message': "not found".format("module action"), 'data': {}},
                            status=http_status_codes.HTTP_404_NOT_FOUND)
        serializer = UserUpdateSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save(updated_by=16)
            return Response({'message': 'user is successfully updated', 'data': serializer.data},
                            status=http_status_codes.HTTP_200_OK)
        tmp_errors = {key: serializer.errors[key][0] for key in serializer.errors}
        return Response({'message': 'Invalid data', 'error': tmp_errors, 'data': {}},
                        status=http_status_codes.HTTP_400_BAD_REQUEST)

    @jwt_check(module_action_list=[permission.user_update])
    def delete(self, request, id=None):
        self.User.objects.filter(id=id).update(is_deleted=True)
        return Response({'message': 'user is successfully deleted', 'data': {}},
                        status=http_status_codes.HTTP_200_OK)



