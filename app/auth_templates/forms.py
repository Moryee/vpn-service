from django.contrib.auth import get_user_model
from django import forms
from users.models import CustomUser


User: CustomUser = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def get_user(self):
        return User.objects.get(email=self.cleaned_data.get("email"))

    def is_valid(self) -> bool:
        valid = super(LoginForm, self).is_valid()

        if not valid:
            return valid

        try:
            user = User.objects.get(email=self.cleaned_data.get("email"))
        except User.DoesNotExist:
            self.add_error("email", "User does not exist")
            return False

        if not user.check_password(self.cleaned_data.get("password")):
            self.add_error("password", "Incorrect password")
            return False

        return True


class RegisterForm(forms.Form):
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def is_valid(self) -> bool:
        valid = super(RegisterForm, self).is_valid()

        if not valid:
            return valid

        if User.objects.filter(email=self.cleaned_data.get("email")).exists():
            self.add_error("email", "User already exists")
            return False

        if self.cleaned_data.get("password1") != self.cleaned_data.get("password2"):
            self.add_error("password2", "Passwords do not match")
            return False

        return True

    def save(self, commit=True):
        print(self.cleaned_data)
        user = User.objects.create_user(
            email=self.cleaned_data.get("email"),
            password=self.cleaned_data.get("password1"),
        )
        return user
