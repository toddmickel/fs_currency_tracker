from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
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
    template_name = 'profile2.html'

    def form_valid(self, form):
        self.object.save()
        messages.success(self.request, 'Profile Successfully Updated')
        return super().form_valid(form)



