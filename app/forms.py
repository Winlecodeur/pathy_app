from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Post, Categorie,Comment_Event,Comment_Post,Messagerie,Compte,Event,NEWSLETTER, Reservation,Service,Mannequin,Agenda,Client
from django.core.exceptions import ValidationError

class PasswordResetForm(forms.ModelForm)  :
    email = forms.EmailField(label="votre adresse e-mail", max_length=300, required=True)
class MessageForm(forms.ModelForm):
    class Meta :
        model = Messagerie
        fields = ['image', 'text']


class ProfileForm(forms.ModelForm):
    class Meta :
        model = Profile
        fields = ['image', 'contry','number', 'sex','state','birth','bio', 'adress', 'compte','facebook','whatsapp','instagram']
        widgets = {
            'birth' : forms.DateInput(attrs={
                'type' : 'date-local',
                'class' : 'form-control'
            })
        }


class PostForm(forms.ModelForm):
    class Meta :
        model  = Post
        fields = ['image', 'title', 'bio', 'categorie']

class PostMForm(forms.ModelForm):
    class Meta :
        model  = Post
        fields = ['image', 'title', 'bio']

class CategorieForm(forms.ModelForm):
    class Meta :
        model = Categorie
        fields = ['name']

class CompteForm(forms.ModelForm):
    class Meta :
        model = Compte
        fields = ['name']

class Comment_EventForm(forms.ModelForm):
    class Meta :
        model = Comment_Event
        fields = ['bio']

class Comment_PostForm(forms.ModelForm):
    class Meta :
        model = Comment_Post
        fields = ['bio']

class EventForm(forms.ModelForm):
    class Meta :
        model = Event
        fields = ['image', 'title', 'bio', 'adress', 'date_event','price']
        widgets = {
            'date_event' : forms.DateTimeInput(attrs={
                'type' : 'datetime-local',
                'class' : 'form-control'
            })
        }

class NewsForm(forms.ModelForm):
    class Meta :
        model = NEWSLETTER
        fields = ['email']
        labels = {
            'email' : 'votre adresse email'
        }
        widgets = {
            'email' : forms.EmailInput(attrs= {
                'placeholder'  :'entrez votre email ',
                'class' : 'form-control'
            })
        }

        

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=250,help_text="necessite un email valid ")
    class Meta :
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists() : 
            raise  ValidationError ("un compte avec cet email existe déjà")
        return email

class ProfilUserForm(forms.ModelForm):
    class Meta :
        model = User
        fields = ('first_name', 'last_name','username', 'email')

class ServiceForm(forms.ModelForm):
    class Meta :
        model = Service
        fields = ('name', 'price')

class MannequinForm(forms.ModelForm):
    class Meta :
        model = Profile
        fields = ['compte']

class ReservationForm(forms.ModelForm):
    class Meta :
        model = Reservation
        fields = ( 'service','date', 'bio')
        widgets = {
            'date' : forms.DateTimeInput(attrs={
                'type' : 'datetime-local',
                'class' : 'form.control '
            })
        }

class AgendaForm(forms.ModelForm):
    class Meta :
        model = Agenda
        fields = ('title','client','date', 'bio')
        widgets = {
            'date' : forms.DateTimeInput(attrs={
                'type' : 'datetime-local',
                'class' : 'form-control'
            })
        }


class ClientForm(forms.ModelForm):
    class Meta : 
        model = Client
        fields = ['user', 'pay', 'bio','service']
