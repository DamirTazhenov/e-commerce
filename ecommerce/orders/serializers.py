from rest_framework import serializers
from .models import Order, OrderItem
from products.serializer import ProductSerializer
from users.serializers import UserSerializer

from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'total_amount', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        # First, create the order with a default total_amount (0)
        order = Order.objects.create(user=validated_data['user'], total_amount=0)

        total_amount = 0
        # Now, calculate the total amount from the order items
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            price = item_data['price']
            total_amount += price * quantity
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)

        # Finally, update the total_amount
        order.total_amount = total_amount
        order.save()

        return order