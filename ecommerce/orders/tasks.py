from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Order
from django.core.exceptions import ObjectDoesNotExist


@shared_task(queue='emails')
def send_order_confirmation_email(user_email, order_id):
    try:
        order = Order.objects.select_related('user').prefetch_related('items__product').get(id=order_id)
        user = order.user

        subject = f'Order Confirmation - {order.id}'
        message = f'Thank you for your order! Your order ID is {order.id}.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user_email]

        html_message = render_to_string('email_templates/order_confirmation.html', {
            'user': user,
            'order': order,
            'items': order.items.all(),
        })

        send_mail(subject, message, email_from, recipient_list, html_message=html_message)

    except Order.DoesNotExist:
        raise ValueError(f"Order with ID {order_id} does not exist.")


def payment_gateway_process(order):
    return True


@shared_task
def process_order(order_id):
    try:
        order = Order.objects.get(id=order_id)
        for item in order.items.all():
            product = item.product
            if product.stock_quantity < item.quantity:
                raise ValueError(f"Not enough stock for {product.name}")
            product.stock_quantity -= item.quantity
            product.save()

        if not payment_gateway_process(order):
            raise ValueError("Payment failed.")

        order.order_status = 'Processed'
        order.save()

    except ObjectDoesNotExist:
        raise ValueError(f"Order with ID {order_id} does not exist")
