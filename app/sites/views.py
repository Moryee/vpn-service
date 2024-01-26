from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Site
from .forms import SiteForm


class SiteListView(LoginRequiredMixin, View):
    model = Site
    template_name = 'sites/site_list.html'
    context_object_name = 'sites'

    def get_queryset(self):
        return self.model.objects.all().filter(user=self.request.user)

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        context = {
            self.context_object_name: self.get_queryset(),
            'form': SiteForm()
        }
        return render(request, self.template_name, context)


class SiteDetailView(LoginRequiredMixin, View):
    template_name = 'sites/site_update.html'
    context_object_name = 'form'

    def get(self, request: HttpRequest, pk, *args: str, **kwargs: Any) -> HttpResponse:
        site = get_object_or_404(Site, pk=pk)

        if site.user != request.user:
            return redirect(reverse('sites:site-list'))

        form = SiteForm(instance=site)
        return render(request, self.template_name, {'form': form, 'site': site})


class SiteCreateView(LoginRequiredMixin, View):
    success_url = reverse_lazy('sites:site-list')

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = SiteForm(request.POST)
        if form.is_valid():
            site: Site = form.save(commit=False)
            site.user = request.user
            site.save()
            return redirect(self.success_url)
        else:
            message = form.errors
            messages.error(request, 'There is form errors', extra_tags='alert alert-danger')
            messages.error(request, message, extra_tags='alert alert-danger')
            return redirect(self.success_url)


class SiteUpdateView(LoginRequiredMixin, View):
    success_url = reverse_lazy('sites:site-list')

    def post(self, request: HttpRequest, pk, *args: str, **kwargs: Any) -> HttpResponse:
        site = get_object_or_404(Site, pk=pk)

        if site.user != request.user:
            return redirect(reverse('sites:site-list'))

        form = SiteForm(request.POST, instance=site)
        if form.is_valid():
            site: Site = form.save(commit=False)
            site.user = request.user
            site.save()
            return redirect(self.success_url)
        else:
            message = form.errors
            messages.error(request, 'There is form errors', extra_tags='alert alert-danger')
            messages.error(request, message, extra_tags='alert alert-danger')
            return redirect(self.success_url)


class SiteDeleteView(LoginRequiredMixin, DeleteView):
    model = Site
    template_name = 'sites/site_confirm_delete.html'
    success_url = reverse_lazy('sites:site-list')

    def post(self, request, *args: str, **kwargs):
        site: Site = self.get_object()

        if site.user != request.user:
            return redirect(reverse('sites:site-list'))

        response = super().post(request, *args, **kwargs)

        if response.status_code < 400:
            message = f'Site {site.name} was deleted'
            messages.success(request, message, extra_tags='alert alert-success')

        return response
