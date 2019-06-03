from django.conf.urls import url
from apps.jwtimple.view import user, role,moduleaction,category,product
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)


urlpatterns = [

   url(r'^api/token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   url(r'^api/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
   url(r'^user-login', user.Userlogin.as_view()),
   url(r'^user-logout', user.Userlogout.as_view()),

   url(r'^user-registration/(?P<id>[0-9]+)', user.UserDetailApi.as_view(), name='roleDetail'),
   url(r'^user-registration', user.UserRegistration.as_view()),

   url(r'^user-list', user.UserRegistration.as_view()),

   url(r'^user-role-module-action/', moduleaction.RoleModuleActionApiView.as_view()),
   url(r'^user-role/(?P<id>[0-9]+)', role.RoleDetailView.as_view(), name='roleDetail'),
   url(r'^user-role', role.RoleApiView.as_view(), name='roleApi'),


   url(r'^user-module-action/(?P<id>[0-9]+)', moduleaction.ModuleActionDetailView.as_view()),
   url(r'^user-module-action',moduleaction.ModuleActionApiView.as_view()),

   url(r'^category/(?P<id>[0-9]+)', category.CategoryDetailApiView.as_view()),
   url(r'^category', category.CategoryApiView.as_view()),

   url(r'^product/(?P<id>[0-9]+)', product.ProductDeatilApiView.as_view()),
   url(r'^product',product.ProductApiView.as_view()),

]