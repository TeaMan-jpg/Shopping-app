from django.dispatch import receiver
from django.contrib.auth.models import User
from  django.db.models.signals import post_save
import stripe

from shopping.models import Basket, Profiles
@receiver(post_save,sender=User)
def create_basket(created,instance,sender,**kwargs):
    if created:
        Basket.objects.create(user=instance)


@receiver(post_save,sender=User)
def update_basket(created,instance,sender,**kwargs):
    if created == False:
        try:
            instance.basket.save()
        except:
            Basket.objects.create(user=instance)

# @receiver(post_save,sender=User)
# def create_profile(created,instance,sender,**kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(post_save,sender=User)
# def update_profile(created,instance,sender,**kwargs):
#     if not created:
#         try:
#             instance.profile.save()

#         except:
#             Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_stripe_customer(sender, instance, created, **kwargs):
    
    if created:
        try:
            # Create a new Stripe customer
            customer = stripe.Customer.create(
                email=instance.email,
                name=f"{instance.first_name} {instance.last_name}",
                metadata={"user_id": instance.id}
            )

            # Create and link a StripeCustomer instance to the user
            Profiles.objects.create(
                user=instance,
                stripe_customer_id=customer.id
            )
        except stripe.error.StripeError as e:
            # Handle Stripe error (you can add logging or notifications here)
            print(f"Stripe Error: {e}")
