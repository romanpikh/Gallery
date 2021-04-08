from rest_auth.registration.views import RegisterView

# Create your views here.
from apps.users.serializer import CustomsRegistrationSerializer


class RegistrationView(RegisterView):
    serializer_class = CustomsRegistrationSerializer

