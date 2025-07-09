from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, OrderViewSet, StripePaymentView,LoginApiView
#
router = DefaultRouter()
router.register('orders', OrderViewSet, basename='orders')
urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    # path('auth/register/', RegisterView.as_view()),
    path('api/login/', LoginApiView.as_view()),
    path('payment/checkout/', StripePaymentView.as_view()),
]



