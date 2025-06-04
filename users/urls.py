from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from django.urls import path,include
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'user-pan', UserPANViewSet, basename='user-pan')

urlpatterns = router.urls + [
    path('api/', include(router.urls)),
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('login/', LoginOTPView.as_view(), name='login'),
    path('login-verify-otp/', VerifyLoginOTPView.as_view(), name='login-verify-otp'),
    path('pan',PANRegisterView.as_view(),name='pan'),

    path('investsearch/',SearchView.as_view(), name='investsearch'),
    path('investdata/',SearchDataView.as_view(), name='investdata'),
    path('selectsip',SIPView.as_view(), name='selectsip'),
]
