from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


class BakendEmail(ModelBackend):
    def authenticate(self, request, username=None , password=None):
        try:
            user = get_object_or_404(get_user_model(),Q(phone_number = username) | Q(email=username))
            # user = get_user_model().objects.filter(Q(phone_number = username) | Q(email=username))
            if user and user.check_password(password):
                return user
        except:
            return None

