# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User, UserPAN
import requests
from rest_framework.response import Response
import uuid

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to Flashfund – Registration Successful!"
        message = f"""Dear {instance.name or instance.username},

Your registration was successful. We're excited to have you on board!

You can now log in and explore our services.

Thank you for joining us!

Team FlashFund
"""
        recipient_list = [instance.email]
        from_email = settings.EMAIL_HOST_USER

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

# @receiver(post_save, sender=UserPAN)
# def KYCChecker(sender,instance, created, **kwargs):
#     if created:
#         ondc_url = 'https://investment.preprod.vyable.in/ondc/search/'
#         transaction_id = str(uuid.uuid4())
#         message_id = str(uuid.uuid4())
#         try:
#             response=requests.post(ondc_url,transaction_id=transaction_id,message_id=message_id)

#             if response.status_code=="200":
#                 ondc_url = 'https://investment.preprod.vyable.in/ondc/on_searchdata'
#                 try:
#                     response=requests.post(ondc_url,json=request.data,headers={'Authorization': request.headers.get('Authorization'),
#                         'Content-Type': 'application/json'})
#                     response.raise_for_status() 
#                     return Response(response.json(), status=response.status_code)
#                 except requests.exceptions.RequestException as e:
#                       return Response({"error": f"ONDC API error: {str(e)}"}, status=502)
            
#         except Exception as e:
#             return Response({"error": str(e)}, status=500)