from django.forms import BaseModelForm
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from typing import Any

from .forms import RegisterUserForm, LoginUserForm

from core.application.services.internal.user_management import *

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'user_management/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return register_user_get_context_data(self.request, context)
    
    def form_valid(self, form: BaseModelForm) -> JsonResponse:
        if self.request.method == 'POST' and self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            object = form.save()
            object.backend = 'user_management.backends.EmailBackend'
            login(self.request, object)
            return JsonResponse({'status': 'succeed'})
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        if self.request.method == 'POST' and self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': f'{form.errors}'})
        return super().form_invalid(form)
    
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'user_management/login.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return login_user_get_context_data(self.request, context)
    
    def form_valid(self, form):
        user = form.get_user()
        user.backend = 'user_management.backends.EmailBackend'
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm):
        if self.request.method == 'POST' and self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials.'})
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('home')
    
def logout_user(request):
    logout(request)
    return redirect('home')
