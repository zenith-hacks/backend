# registration/forms.py
from allauth.account.forms import SignupForm
from allauth.account.utils import perform_login, filter_users_by_email, assess_unique_email
from allauth.account.adapter import get_adapter
from django.contrib.auth import get_user_model
from allauth.account.internal import flows
from django import forms
from .models import *

class UnifiedSignupLoginForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["password1"]

    def validate_unique_email(self, value):
        adapter = get_adapter()
        assessment = assess_unique_email(value)
        if assessment is True:
            # All good.
            pass
        elif assessment is False:
            # Fail right away.
            pass
        else:
            assert assessment is None
            self.account_already_exists = True
        return adapter.validate_unique_email(value)

    def save(self, request):
        email = self.cleaned_data['email']
        user_model = get_user_model()
        print(filter_users_by_email(email))
        if filter_users_by_email(email) != []:
            flows.login_by_code.request_login_code(self.request, email)
        else:
            user = super(UnifiedSignupLoginForm, self).save(request)
            get_adapter(request).add_message(request, 'account/messages/email_confirmation_sent.txt', email)

        return user

class InformationForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = '__all__'
        exclude = ['user', 'address_geo', 'distance',]

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flights
        fields = '__all__'
        exclude = ['user', 'flights', 'price']