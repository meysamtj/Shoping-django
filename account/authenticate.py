from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None,email=None, password=None,otpcode=None,otp_code_send=None,**kwargs):
        try:
            if email :
                print('auth')
                email_get = get_user_model().objects.get(email= email)
                # otp_code=request.session.get("otp_code")
                print(otp_code_send)
                print(otpcode)
                if email_get and otpcode == otp_code_send:
                    email_get.is_active=True
                    email_get.save()
                    print('auth2')
                    return email_get
            user = get_user_model().objects.get(Q(username=username) | Q(phone_number=username))
            if user and user.check_password(password):
                return user
            # otp_email = request.session.get("otp_code")
            
            
            
        except:
            return None
