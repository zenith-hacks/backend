import allauth.account.forms

class CustomSignupForm(allauth.account.forms.SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["password1"]

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomSignupForm, self).save(request)

        # Add your own processing here.
        user.set_unusable_password()
        user.save()
        # You must return the original result.
        return user

