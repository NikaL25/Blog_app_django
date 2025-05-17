from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['email'].initial = self.instance.user.email
