from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import Tickets, Customer, Agent

class Booking(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = '__all__'

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = '__all__'        
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    user_name = forms.CharField(max_length = 20)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']