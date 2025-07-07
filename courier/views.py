from rest_framework import generics
from .serializers import RegisterSerializer,OrderSerializer
from .models import User,Order
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
import stripe
from django.conf import settings


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer



class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class IsDeliveryMan(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'delivery'

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ['assign_delivery', 'list_all']:
            return [IsAdmin()]
        elif self.action in ['update_status', 'my_deliveries']:
            return [IsDeliveryMan()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Order.objects.all()
        elif user.role == 'delivery':
            return Order.objects.filter(assigned_delivery_man=user)
        return Order.objects.filter(user=user)

    @action(detail=True, methods=['put'])
    def assign_delivery(self, request, pk=None):
        order = self.get_object()
        delivery_id = request.data.get('delivery_man_id')
        try:
            delivery_man = User.objects.get(id=delivery_id, role='delivery')
            order.assigned_delivery_man = delivery_man
            order.status = 'assigned'
            order.save()
            return Response({"message": "Delivery man assigned."})
        except:
            return Response({"error": "Invalid delivery man ID."}, status=400)

    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        if order.assigned_delivery_man != request.user:
            return Response({"error": "Unauthorized."}, status=403)
        status = request.data.get('status')
        if status not in ['delivered', 'completed']:
            return Response({"error": "Invalid status."}, status=400)
        order.status = status
        order.save()
        return Response({"message": f"Status updated to {status}."})



from decouple import config
from rest_framework.views import APIView

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripePaymentView(APIView):
    def post(self, request, format=None):
        try:
            order_id = request.data.get('order_id')
            order = Order.objects.get(id=order_id, user=request.user)

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': f'Order #{order.id}'},
                        'unit_amount': int(order.delivery_fee * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://example.com/success',
                cancel_url='https://example.com/cancel',
            )
            return Response({'checkout_url': session.url})
        except Exception as e:
            return Response({'error': str(e)}, status=400)

