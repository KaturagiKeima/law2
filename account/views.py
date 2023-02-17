from django.http.response import HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import SignUpForm

class LoginView(LoginView):

    template_name = 'account/login.html'
    form_class = AuthenticationForm

class SignUpView(CreateView):

    form_class = SignUpForm
    template_name = "account/signup.html"
    success_url = reverse_lazy("law:index")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())