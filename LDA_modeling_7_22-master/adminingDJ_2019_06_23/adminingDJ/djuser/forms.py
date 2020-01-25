from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import (authenticate, get_user_model)

User = get_user_model()


class SignInForm(forms.Form):
    username = forms.CharField(label=False, max_length=40, widget=forms.TextInput(
        attrs={'placeholder': 'Username|Email|Phone',
               'class': 'form-control', 'autocomplete': 'off'}
    ))
    password = forms.CharField(label=False, max_length=40, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'class': 'form-control'}
    ))
    remember_me = forms.BooleanField(required=False)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError(
                    'We could not verify your credentials.')

        return super(SignInForm, self).clean(*args, **kwargs)


class SignUpForm(forms.ModelForm):
    username = forms.CharField(label=False, max_length=16, widget=forms.TextInput(
        attrs={'placeholder': 'Username',
               'class': 'form-control', 'autocomplete': 'off'}
    ))
    password = forms.CharField(label=False, max_length=40, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password',
               'class': 'form-control', 'autocomplete': 'off'}
    ))
    re_password = forms.CharField(label=False, max_length=40, widget=forms.PasswordInput(
        attrs={'placeholder': 'Re password',
               'class': 'form-control', 'autocomplete': 'off'}
    ))
    full_name = forms.CharField(
        label=False, max_length=40, widget=forms.TextInput(
            attrs={'placeholder': 'Fullname',
                   'class': 'form-control', 'autocomplete': 'off'}
        )
    )
    email = forms.EmailField(
        label=False, max_length=100, widget=forms.EmailInput(
            attrs={'placeholder': 'Email',
                   'class': 'form-control', 'autocomplete': 'off'}
        )
    )
    contact_no = forms.CharField(label=False, max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Contact No',
               'class': 'form-control', 'autocomplete': 'off'}
    ))
    #organization = forms.CharField()
    #organization = forms.CharField()
    #terms = forms.CheckboxInput()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'full_name',
            'password',

        ]

    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if password != re_password:
            raise forms.ValidationError('Passwords must match.')

        username = self.cleaned_data.get('username')
        username_qs = User.objects.filter(username=username)

        if username_qs.exists():
            raise forms.ValidationError('This username is already being used.')

        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email)

        if email_qs.exists():
            raise forms.ValidationError('This email is already being used.')

        return super(SignUpForm, self).clean(*args, **kwargs)


class RecoverPassForm(forms.Form):
    pass
