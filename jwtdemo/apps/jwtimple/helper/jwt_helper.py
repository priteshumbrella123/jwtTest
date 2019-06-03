from apps.jwtimple.serilizer.TokenSerilizer import MyTokenObtainPairSerializer
from rest_framework.views import Response
from rest_framework import status as http_status_codes


def get_my_token(user_detail):
    my_token = MyTokenObtainPairSerializer()
    data = my_token.validate(user_detail)
    return data


class jwt_check(object):

    def __init__(self, module_action_list=[]):
        self.module_action_list = module_action_list

    def __call__(self, func, *args, **kwargs):
        def wrap(class_obj, *args, **kwargs):
            try:
                request_token = class_obj.request.META.get('HTTP_AUTHORIZATION',None)

                if not request_token:
                    return Response({'message': 'please login first to access url', 'data': {}},
                                status=http_status_codes.HTTP_400_BAD_REQUEST)

                elif set(self.module_action_list) <= set(class_obj.request.user.get_all_module_actions):

                    return func(class_obj, *args, **kwargs)

                else:
                    return Response({'message': 'you are not authorized to this url (permission denied).', 'data': {}},
                                        status=http_status_codes.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'message': 'Server error.', 'error': {'error':str(e)}, 'data': {}},
                            status=http_status_codes.HTTP_500_INTERNAL_SERVER_ERROR)


        return wrap