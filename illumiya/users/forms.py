from django import forms
from django.contrib.auth.models import User

from django_registration.forms import RegistrationForm

from .models import Profile, USER_TYPE_CHOICES

class CustomRegistrationForm(RegistrationForm):
    username = forms.CharField(required=False)
    name = forms.CharField(max_length=50)
    mobile_number = forms.CharField(max_length=14)
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)


    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email'].strip()).exists():
            raise forms.ValidationError('The email is already used.')
        return self.cleaned_data['email']

    """def save(self, *args, **kwargs):
        data = self.cleaned_data
        user = User(username=data['email'],
                    email=data['email'])
        user.save()"""

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    street = forms.CharField(max_length=150)

    class Meta:
        model = Profile
        exclude = ('user', 'user_type', 'profile_pic')