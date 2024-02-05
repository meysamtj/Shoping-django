
# from src.celery import app
# from celery import shared_task
# from django.core.mail import send_mail
# from datetime import datetime, timedelta
# from django.utils import timezone
# from .models import CustomUser
# @app.task
# def send_otp_to_phone_number_task(destination, otp):
#     send_mail(
#                     'Shop',
#                     f' ACTIVE CODE : {otp}',
#                     'setting.EMAIL_HOST_USER',
#                     [destination],
#                     fail_silently=False
#                 )

# @shared_task   
# def delete_users():
#     user = CustomUser.objects.all()
#     for usr in user:
#         if usr.is_active == False:
#             # usr.hard_delete()
#             if usr.created_at + timedelta(days=3) < timezone.now():
#                 usr.hard_delete()
                
        