from django.contrib.auth import get_user_model
from django.forms import ModelForm
from users.models import CustomUser
from .models import Site


User: CustomUser = get_user_model()


class SiteForm(ModelForm):
    class Meta:
        model = Site
        fields = ['name', 'url']
