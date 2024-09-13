from django.db.models.signals import Signal, post_save

from .models import Customer, Order
from django.dispatch import receiver
from .utils import sendEmail

customer_signal = Signal()
msg = """

        <html lang="en">

        <body>
        <img src="cid:ZesstaLogo" width="150px" />
        <h1>Zessta eComm</h1>
        <p>
            msg_area
        </p>
        <br />
        <p>Thank you for using Zessta Software Services.</p>
        <br />
        <p>
            Regards,<br />
            Zessta Software Services, Hyderabad,
        </p>
        </body>
        </html>

        """


@receiver(post_save, sender=Customer)
def customer_action(sender, instance, created, *args, **kwargs):
    if created:

        subject = "User Profile Created - Zessta"
        replacewith = "Dear {customer}, Your profile has been sucessfully created at our portal".format(
            customer=instance
        )
        msg_send = msg.replace("msg_area", replacewith)
        sendEmail(instance.customer_email, instance, msg_send, subject, None)

    else:
        print("Update", instance.customer_mobile)

        subject = "User Profile Update - Zessta"

        replacewith = "Dear {customer}, Your profile has been sucessfully updated at our portal".format(
            customer=instance
        )
        msg_send = msg.replace("msg_area", replacewith)
        sendEmail(instance.customer_email, instance, msg_send, subject, None)


@receiver(post_save, sender=Order)
def order_action(sender, instance, created, *args, **kwargs):
    if created:
        print("Sending Order Message")

        subject = "Order Placed Created - Zessta"
        replacewith = "Dear {customer}, Your Order has been sucessfully Placed".format(
            customer=instance.customerID
        )
        msg_send = msg.replace("msg_area", replacewith)
        sendEmail(
            instance.customerID.customer_email,
            instance.customerID,
            msg_send,
            subject,
            None,
        )
        
        
        for product in instance.customer_ordered_products.all():
            product.product_quantity = F('product.product_quantity') -1
            product.save()

    else:
        print("Order Status Email Triggered")
        subject = "Order Status - Zessta"
        replacewith = "Dear {customer}, Your Order status has been changed to {order_status}".format(
            customer=instance.customerID, order_status=instance.customer_order_status
        )
        msg_send = msg.replace("msg_area", replacewith)
        sendEmail(
            instance.customerID.customer_email,
            instance.customerID,
            msg_send,
            subject,
            None,
        )
