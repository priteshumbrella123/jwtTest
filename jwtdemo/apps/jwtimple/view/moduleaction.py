from rest_framework.views import APIView
from rest_framework.response import Response
from apps.jwtimple.serilizer.ModuleActionSerializer import ModuleActionSerializer,RoleModuleActionSerializer
from rest_framework import status as http_status_codes
from apps.jwtimple.models import ModuleAction
from apps.jwtimple.helper.jwt_helper import jwt_check
from apps.jwtimple.helper import permission


class ModuleActionApiView(APIView):

    @jwt_check(module_action_list=[permission.module_action_create])
    def post(self, request):
        data = request.data
        serializer = ModuleActionSerializer(data=data)
        if serializer.is_valid():
            serializer.save(created_by= request.user.id)
            return Response({'message': 'module action is successfully created', 'data': serializer.data},
                            status=http_status_codes.HTTP_201_CREATED)
        tmp_errors = {key: serializer.errors[key][0] for key in serializer.errors}
        return Response({'message': 'Invalid data', 'error': tmp_errors, 'data': {}},
                    status=http_status_codes.HTTP_400_BAD_REQUEST)

    @jwt_check(module_action_list=[permission.module_action_list])
    def get(self, request):
        queryset = ModuleAction.objects.filter(is_deleted=False).order_by('-id')
        serializer = ModuleActionSerializer(queryset, many=True)
        return Response(
            {'message': "get all module action", 'data': serializer.data}, status=http_status_codes.HTTP_200_OK)


class ModuleActionDetailView(APIView):

    def get_object(self, id):
        try:
            return ModuleAction.objects.get(id=id)
        except ModuleAction.DoesNotExist as e:
            return False

    @jwt_check(module_action_list=[permission.module_action_detail])
    def get(self, request, id=None):
        instance = self.get_object(id)
        if not instance:
            return Response({'message': "not found".format("module action"), 'data': {}},
                            status=http_status_codes.HTTP_404_NOT_FOUND)
        serializer = ModuleActionSerializer(instance)
        return Response({'message': 'get module action', 'data': serializer.data}, status=http_status_codes.HTTP_200_OK)

    @jwt_check(module_action_list=[permission.module_action_update])
    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        if not instance:
            return Response({'message': "not found".format("module action"), 'data': {}},
                            status=http_status_codes.HTTP_404_NOT_FOUND)
        serializer = ModuleActionSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save(updated_by= request.user.id)
            return Response({'message': 'module action is successfully updated', 'data': serializer.data},
                            status=http_status_codes.HTTP_200_OK)
        tmp_errors = {key: serializer.errors[key][0] for key in serializer.errors}
        return Response({'message':'Invalid data','error': tmp_errors, 'data': {}},
                        status=http_status_codes.HTTP_400_BAD_REQUEST)
    @jwt_check(module_action_list=[permission.module_action_delete])
    def delete(self, request, id=None):
        ModuleAction.objects.filter(id=id).update(is_deleted=True)
        return Response({'message': 'module action is successfully deleted', 'data': {}},
                        status=http_status_codes.HTTP_200_OK)


##################################  RoleModuleAction API ###############################################

class RoleModuleActionApiView(APIView):

    def post(self, request):

        data = request.data
        serializer = RoleModuleActionSerializer(data=data)
        if serializer.is_valid():
            resp = serializer.save(created_by= request.user.id)
            return Response({'message': 'Permission {}'.format(resp["message"]), 'data': {}},
                                status=http_status_codes.HTTP_201_CREATED)
        tmp_errors = {key: serializer.errors[key][0] for key in serializer.errors}
        return Response({'message':'Invalid data','error': tmp_errors, 'data': {}}, status=http_status_codes.HTTP_400_BAD_REQUEST)
