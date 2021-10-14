from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from .forms import ProfileForm
from .models import CustomUser



class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class ProfileView(LoginRequiredMixin, generic.edit.UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = 'profile.html'

    def form_valid(self, form):
        self.object.save()
        messages.success(self.request, 'Profile Successfully Updated')
        return super().form_valid(form)

