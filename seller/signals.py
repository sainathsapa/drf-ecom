from django.db.models.signals import Signal, post_save

from .models import Product
from django.dispatch import receiver
from customer.utils import sendEmail

seller_signal = Signal()
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


@receiver(post_save, sender=Product)
def product_action(sender, instance, created, *args, **kwargs):
   
    if instance.product_quantity < 1:
        print("Low Product Trigger")

        subject = "Low Stock {product} - Zessta".format(product=instance)
        for i in instance.products_sellers.all():
            
            replacewith = "Dear {seller}, {product} is Low in Stock".format(
                product=instance,
                seller=i.seller_name
            )
            msg_send = msg.replace("msg_area", replacewith)
            sendEmail(i.seller_email, instance, msg_send, subject, None)

