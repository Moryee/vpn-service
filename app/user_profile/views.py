from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


class Index(LoginRequiredMixin, View):
    template_name = 'user_profile/index.html'

    def get(self, request, *args, **kwargs):

        context = {
            'user': request.user
        }
        return render(request, self.template_name, context)
