from rest_framework.views import APIView
from rest_framework.response import Response
from apps.jwtimple.serilizer.Roleserializer import RoleSerializer
from rest_framework import status as http_status_codes
from apps.jwtimple.models import Role
from apps.jwtimple.helper.jwt_helper import jwt_check
from apps.jwtimple.helper import permission


class RoleApiView(APIView):

    @jwt_check(module_action_list=[permission.role_create])
    def post(self, request):
        data = request.data
        serializer = RoleSerializer(data=data)
        if serializer.is_valid():
            serializer.save(created_by= request.user.id)
            return Response({'message': 'role is successfully created', 'data': serializer.data},
                            status=http_status_codes.HTTP_201_CREATED)
        tmp_errors = {key: serializer.errors[key][0] for key in serializer.errors}
        return Response({'message': 'Invalid data', 'error': tmp_errors, 'data': {}},
                        status=http_status_codes.HTTP_400_BAD_REQUEST)

    #@jwt_check(module_action_list=[permission.role_list])
    def get(self,request):
        print(request.user.get_all_module_actions)
        data = Role.objects.filter(is_active = True, is_deleted = False).order_by('-id')
        #data['module_action'] = request.user.get_all_module_actions
        serializer = RoleSerializer(data, many=True)
        return Response(
            {'message': "Role list", 'data': serializer.data}, status=http_status_codes.HTTP_200_OK)


class RoleDetailView(APIView):

    def get_object(self, id):
        try:
            return Role.objects.get(id=id)
        except Role.DoesNotExist as e:
            return False

    @jwt_check(module_action_list=[permission.role_detail])
    def get(self, request, id=None):
        instance = self.get_object(id)
        if not instance:
            return Response({'message': "{} not found ".format("Role"), 'data': {}},
                            status=http_status_codes.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(instance)
        return Response({'message': 'get role', 'data': serializer.data}, status=http_status_codes.HTTP_200_OK)

    @jwt_check(module_action_list=[permission.role_update])
    def put(self, request, id=None):

        data = request.data
        instance = self.get_object(id)
        if not instance:
            return Response({'message': "{} not found".format("Role"), 'data': {}},
                            status=http_status_codes.HTTP_404_NOT_FOUND)
        serializer = RoleSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save(updated_by= request.user.id)
            return Response({'message': 'role is successfully updated', 'data': serializer.data}, status=http_status_codes.HTTP_200_OK)
        tmp_errors = {key: serializer.errors[key][0] for key in serializer.errors}
        return Response({'message':'Invalid data','error': tmp_errors, 'data': {}}, status=http_status_codes.HTTP_400_BAD_REQUEST)

    @jwt_check(module_action_list=[permission.role_delete])
    def delete(self, request, id=None):
        Role.objects.filter(id=id).delete()
        return Response({'message': 'role is successfully deleted', 'data': {}}, status=http_status_codes.HTTP_200_OK)