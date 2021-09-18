from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileForm
from django.urls import reverse_lazy
from django.views import generic
from .models import CustomUser



class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class ProfileView(LoginRequiredMixin, generic.edit.UpdateView):
    model = CustomUser
    form_class = ProfileForm
    success_url = reverse_lazy('home')
    template_name = 'profile.html'

    def form_valid(self, form):
        return super().form_valid(form)



