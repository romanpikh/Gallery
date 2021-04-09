from django.urls import path, re_path
from rest_auth.registration.views import VerifyEmailView
from rest_auth.views import LoginView

from apps.users.views import RegistrationView

urlpatterns = [
    path('signup/', RegistrationView.as_view(), name='account_signup'),
    path('sigin/', LoginView.as_view(), name="sigin"),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$',
            VerifyEmailView.as_view(), name='account_confirm_email'),

]
