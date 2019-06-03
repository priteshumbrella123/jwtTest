from rest_framework.views import APIView
from rest_framework.response import Response
from apps.jwtimple.serilizer.ProductSerializer import ProductSerializer
from rest_framework import status as http_status_codes
from apps.jwtimple.models import Product
from apps.jwtimple.helper.jwt_helper import jwt_check
from apps.jwtimple.helper import permission


class ProductApiView(APIView):

    @jwt_check(module_action_list=[permission.product_create])
    def post(self, request):
        data = request.data
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'product is successfully created', 'data': serializer.data},
                        status=http_status_codes.HTTP_201_CREATED)
        tmp_errors = {key: serializer.errors[key][0] for key in serializer.errors}
        return Response({'message': 'Invalid data', 'error': tmp_errors, 'data': {}},
                        status=http_status_codes.HTTP_400_BAD_REQUEST)

    @jwt_check(module_action_list=[permission.product_list])
    def get(self, request):

        queryset = Product.objects.filter(is_deleted= False, is_active = True)
        q=request.query_params.get('q', None)
        print(q)
        if q:
            queryset  = Product.objects.filter(category__name__iexact=q)
        serializer = ProductSerializer(queryset, many=True)
        return Response({'message': "get all product", 'data': serializer.data}, status=http_status_codes.HTTP_200_OK)


class ProductDeatilApiView(APIView):

    def get_object_id(self,id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist as e:
            return False

    @jwt_check(module_action_list=[permission.product_detail])
    def get(self, request, id = None):
        instance = self.get_object_id(id)
        if not instance:
            return Response({'message': "not found".format("product"), 'data': {}},
                            status=http_status_codes.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(instance)
        return Response({'message': 'get product', 'data': serializer.data}, status=http_status_codes.HTTP_200_OK)

    @jwt_check(module_action_list=[permission.product_update])
    def put(self, request, id = None):
        data = request.data
        instance = self.get_object_id(id)
        if not instance:
            return Response({'message': "not found".format("product"), 'data': {}},
                            status=http_status_codes.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save(updated_by= request.user.id)
            return Response({'message': 'product is successfully updated', 'data': serializer.data},
                            status=http_status_codes.HTTP_200_OK)
        tmp_errors = {key: serializer.errors[key][0] for key in serializer.errors}
        return Response({'message':'Invalid data','error': tmp_errors, 'data': {}},)

    @jwt_check(module_action_list=[permission.product_delete])
    def delete(self, request, id=None):
        Product.objects.filter(id=id).update(is_deleted=True)
        return Response({'message': 'product is successfully deleted', 'data': {}},
                        status=http_status_codes.HTTP_200_OK)