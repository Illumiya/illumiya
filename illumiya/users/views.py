# Create your views here.

from django.views.generic import View
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login

#from django_registration.backends.activation.views import RegistrationView
from django_registration.backends.one_step.views import RegistrationView

from .forms import CustomRegistrationForm, ProfileForm
from .models import Profile

#clsss SignInView(LoginView):
#    template_name = 'users/login.html'

class CustomRegitrationView(RegistrationView):
    form_class = CustomRegistrationForm

    def form_valid(self, form):
        data = form.cleaned_data
        user = form.save(commit=False)
        user.username = data['email']
        name = data['name'].split(' ', 1)
        if len(name) > 1:
            user.first_name = name[0].strip()
            user.last_name = name[1].strip()
        #user.set_password(data['password'])
        user.save()
        user = authenticate(username=data['email'],
                            password=data['password1'])
        login(self.request, user)
        profile = Profile(user=user,
                          user_type=data['user_type'],
                          mobile_number=data['mobile_number'])
        profile.save()
        return HttpResponseRedirect(reverse('profile'))

class ProfileView(FormView):
    template_name = 'users/profile.html'
    form_class = ProfileForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        try:
            profile = self.request.user.profile
            initial['instance'] = profile
            initial['street'] = profile.street
            initial['city'] = profile.city
            initial['state'] = profile.state
            initial['country'] = profile.country
        except Profile.DoesNotExist:
            pass

        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['email'] = self.request.user.email
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(page='profile')
        return context

    def form_valid(self, form):
        #print(self.request.user, "self.request.user")
        data = form.cleaned_data
        #print(data)
        profile = self.request.user.profile
        #print(profile, "profile")
        profile.street = data['street']
        profile.city = data['city']
        profile.state = data['state']
        profile.country = data['country']
        self.request.user.first_name = data['first_name']
        self.request.user.last_name = data['last_name']
        self.request.user.email = data['email']
        self.request.user.save()
        #profile.user = self.request.user
        profile.save()
        return HttpResponseRedirect(reverse('profile'))