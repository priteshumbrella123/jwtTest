from rest_framework.views import APIView
from rest_framework.response import Response
from apps.jwtimple.serilizer.CategorySerializer import CategorySerializer
from rest_framework import status as http_status_codes
from apps.jwtimple.models import Category
from apps.jwtimple.helper.jwt_helper import jwt_check
from apps.jwtimple.helper import permission


class CategoryApiView(APIView):

    @jwt_check(module_action_list=[permission.category_create])
    def post(self, request):
        data = request.data
        serializer = CategorySerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'category is successfully created', 'data': serializer.data},
                            status=http_status_codes.HTTP_201_CREATED)
        tmp_errors = {key: serializer.errors[key][0] for key in serializer.errors}
        return Response({'message': 'Invalid data', 'error': tmp_errors, 'data': {}},
                        status=http_status_codes.HTTP_400_BAD_REQUEST)

    @jwt_check(module_action_list=[permission.category_list])
    def get(self, request):

        queryset = Category.objects.filter(is_deleted = False, is_active = True)
        serializer = CategorySerializer(queryset, many=True)
        return Response({'message': "get all category", 'data': serializer.data}, status=http_status_codes.HTTP_200_OK)


class CategoryDetailApiView(APIView):

    def get_object_id(self,id):
        try:
            return Category.objects.get(id=id)
        except Category.DoesNotExist as e:
            return False

    @jwt_check(module_action_list=[permission.category_detail])
    def get(self, request, id = None):

        instance = self.get_object_id(id)

        if not instance:
            return Response({'message': "not found".format("category"), 'data': {}},
                            status=http_status_codes.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(instance)
        return Response({'message': 'get category', 'data': serializer.data}, status=http_status_codes.HTTP_200_OK)

    @jwt_check(module_action_list=[permission.category_update])
    def put(self, request, id = None):
        data = request.data
        instance = self.get_object_id(id)
        if not instance:
            return Response({'message': "not found".format("category"), 'data': {}},
                            status=http_status_codes.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save(updated_by= request.user.id)
            return Response({'message': 'category is successfully updated', 'data': serializer.data},
                            status=http_status_codes.HTTP_200_OK)
        tmp_errors = {key: serializer.errors[key][0] for key in serializer.errors}
        return Response({'message':'Invalid data','error': tmp_errors, 'data': {}},)

    @jwt_check(module_action_list=[permission.category_delete])
    def delete(self, request, id=None):
        Category.objects.filter(id=id).update(is_deleted=True)
        return Response({'message': 'category is successfully deleted', 'data': {}},
                        status=http_status_codes.HTTP_200_OK)
