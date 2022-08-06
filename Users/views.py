from rest_framework.views import APIView
from .serializers import RegisterSerializer, ActivateSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from smtplib import SMTPException


class RegisterApiView(APIView):
    def post(self, request):
        serialized_data = RegisterSerializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        user = serialized_data.save()
        try:
            send_mail(
                'Email Confirmation',
                f'your your passcode {user.OTP}',
                settings.EMAIL_FROM,
                (user.email,),
                fail_silently=False,
            )
        except SMTPException:
            return Response('Email not sent:')
        return Response(data={'user': str(user), 'email': user.email, 'id': user.id,
                              'success': 'confirmation mail sent'},
                        status=status.HTTP_201_CREATED)


class ActivateApiView(APIView):
    def put(self, request):
        user_id = request.data.get('uid', None)
        if request.data.get('uid', None):

            serialized_data = ActivateSerializer(data=request.data)
            serialized_data.is_valid(raise_exception=True)