from rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from allauth.account.adapter import get_adapter


from rest_auth.registration.serializers import RegisterSerializer


class CustomsRegistrationSerializer(RegisterSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    def validate_first_name(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_last_name(self, username):
        username = get_adapter().clean_username(username)
        return username

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', '')
        }


class CustomLoginSerializer(LoginSerializer):

    username = None
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.data['user'] = {
            'name': request.user.first_name,
            'username': request.user.username
        }
        request.session['remember_me'] = request.data.get('remember_me', False)
        request.session.modified = True
        return response
