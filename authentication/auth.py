from rest_framework.authentication import BaseAuthentication
from account.models import Session
from django.contrib.auth.models import AnonymousUser

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        access_token =  request.headers.get("Access-Token")
        refresh_token =  request.headers.get("Refresh-Token")

        if access_token:
            session = Session.objects.filter(access_token=access_token).first()
            if session:
                return (session.user, None)

        if refresh_token:
            session = Session.objects.filter(refresh_token=refresh_token).first()
            if session:
                session.update_access_token()
                return (session.user, None)

        return None